from django.shortcuts import render
from django.views import View
from .forms import OrderCommentForm
from .models import Order, Delivery, PayMethod
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from app_users.models import Profile, Role
from app_goods.models import Product
from django.db import transaction
from cart.models import CartItems
from custom_admin.models import DefaultSettings
from django.db.models import Count, F, ExpressionWrapper, FloatField, Sum
from django.db import transaction
from decimal import *
from app_payment.tasks import handle_payment
from custom_admin.views import logger
from app_payment.models import PayStatus
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderView(LoginRequiredMixin, View):
	login_url = reverse_lazy('register')
	
	@staticmethod
	def get(request, **kwargs):
		context = dict()
		
		cart = CartItems.objects.filter(user=request.user.id).select_related(
			'product__discount').annotate(price_discount=ExpressionWrapper(
			F('price') * (1 - F('product__discount__discount_value') * Decimal('1.0') / 100),
			output_field=FloatField()), total_sum=(Sum(F('price') * F('quantity'))),
			total_sum_with_discount=Sum(F('price_discount') * F('quantity')))
		q_shops = CartItems.objects.filter(session_id=request.user.id).aggregate(
			q_shops=Count('shop', distinct=True))
		
		if kwargs.get('pk') == '2':
			cart = CartItems.objects.filter(session_id=request.session.session_key).select_related(
				'product__discount').annotate(price_discount=ExpressionWrapper(
				F('price') * (1 - F('product__discount__discount_value') * Decimal('1.0') / 100),
				output_field=FloatField()), total_sum=(Sum(F('price') * F('quantity'))),
				total_sum_with_discount=Sum(F('price_discount') * F('quantity')))
			q_shops = CartItems.objects.filter(session_id=request.session.session_key).aggregate(
				q_shops=Count('shop', distinct=True))
		total_sum = 0
		total_sum_with_discount = 0
		q = Decimal(10) ** -2
		for product in cart:
			total_sum += Decimal(product.total_sum).quantize(q)
			if product.total_sum_with_discount:
				total_sum_with_discount += Decimal(product.total_sum_with_discount).quantize(q)
			else:
				total_sum_with_discount += Decimal(product.total_sum).quantize(q)
		context['cart'] = cart
		context['total_sum'] = str(total_sum)
		context['total_sum_with_discount'] = str(total_sum_with_discount)
		context['q_shops'] = q_shops['q_shops']
		
		if request.user.is_authenticated:
			user = User.objects.get(id=request.user.id)
			context['user'] = user
			profile = Profile.objects.filter(user_id=request.user.id)
			if profile:
				profile = Profile.objects.get(user_id=request.user.id)
			else:
				role = Role.objects.get(name='покупатель')
				profile = Profile.objects.create(user=user, phone_number='', role=role)
			context['profile'] = profile
		
		return render(request, template_name='order/order.html', context=context)
	
	@staticmethod
	def post(request, **kwargs):
		data = request.POST
		comment = data['comment']
		email = data['mail']
		user = User.objects.get(email=email)
		delivery = Delivery.objects.get(title=data['delivery'])
		city = data['city']
		address = data['address']
		pay_method = PayMethod.objects.get(title=data['pay'])
		
		products = CartItems.objects.filter(session_id=request.session.session_key).select_related('product')
		order_goods = {}
		for product in products:
			if product.shop not in order_goods.keys():
				order_goods[product.shop] = {}
			order_goods[product.shop][product.product_id] = product.quantity
		Order.objects.create(user=user, order_goods=order_goods, delivery=delivery, city=city,
		                     address=address, pay_method=pay_method, order_comment=comment, payment_status='')
		
		if pay_method.id == 1:
			return render(request, template_name='order/payment.html', )
		return render(request, template_name='order/payment_someone.html')


class OrderPayment(View):
	
	@staticmethod
	def post(request):
		card_num = request.POST['numero1'].replace(' ', '')
		user = request.user
		profile = Profile.objects.get(user_id=user.id)
		profile.card = card_num
		profile.save()
		q_shops = CartItems.objects.filter(session_id=request.session.session_key). \
			aggregate(q_shops=Count('shop', distinct=True))['q_shops']
		order = Order.objects.filter(user=user).last()
		payment_amount = order.get_total_cost()
		if order.get_total_cost_with_discount():
			payment_amount = order.get_total_cost_with_discount()
		if order.delivery.id == 1 and (payment_amount < 2000 or q_shops > 1):
			payment_amount += 200
		elif order.delivery.id == 2:
			payment_amount += 500
		handle_payment.delay(order.id, card_num, payment_amount)
		return render(request, template_name='order/progressPayment.html')
	
	@transaction.atomic
	def get(self, request):
		user = request.user
		profile = Profile.objects.get(user_id=user.id)
		order = Order.objects.filter(user=user).select_related('delivery', 'pay_method').last()
		expression_wrapper = ExpressionWrapper(
			F('price') * (1 - F('product__discount__discount_value') * Decimal('1.0') / 100),
			output_field=FloatField())
		cart = CartItems.objects.filter(session_id=request.session.session_key). \
			select_related('product__discount'). \
			annotate(price_discount=expression_wrapper,
		             total_sum=Sum(F('price') * F('quantity')),
		             total_sum_with_discount=Sum(F('price_discount') * F('quantity')))
		if order.payment_status == 'Оплачено':
			for product in cart:
				# shop = Shop.objects.get(name=product.shop)
				shop = Shop.objects.get(slug=product.shop)
				shop_product = ShopProduct.objects.get(product=product.product, shop=shop.id)
				if shop_product.quantity - product.quantity >= 0:
					shop_product.quantity -= product.quantity
					shop_product.save()
				else:
					logger.error(f'Заказ не оформлен. Недостаточное количество товара {product.product}')
					# order.payment_status = f'Недостаточное количество товара {product.product}'
					pay_status = PayStatus.objects.get(title='недостаточное кол-во товаров')
					order.payment_status = pay_status.title
					order.save()
					return render(request, template_name='order/order_detail.html',
					              context={'user': user,
					                       'profile': profile,
					                       'cart': cart,
					                       'order': order
					                       })
			logger.info(f'Оформление заказа {order.id} пользователем {user.id}')
			cart.delete()
			return render(request, template_name='order/order_detail.html',
			              context={'user': user,
			                       'profile': profile,
			                       'order': order
			                       })
		elif order.payment_status:
			logger.error('Ошибка оплаты')
			return render(request, template_name='order/order_detail.html', context={'user': user,
			                                                                         'profile': profile,
			                                                                         'cart': cart,
			                                                                         'order': order
			                                                                         })
		else:
			return render(request, template_name='order/progressPayment.html')


class OrderRepeat(View):
	
	@staticmethod
	def get(request):
		order = Order.objects.filter(user=request.user).last()
		if order.pay_method_id == 1:
			return render(request, template_name='order/payment.html', )
		return render(request, template_name='order/payment_someone.html')
