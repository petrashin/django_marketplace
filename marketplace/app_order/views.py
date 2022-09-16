from django.shortcuts import render, redirect
from django.views import View
from .forms import OrderCommentForm
from .models import Order, Delivery, PayMethod
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from app_users.models import Profile
from app_goods.models import Product
from app_shops.models import Shop, ShopProduct
from cart.models import CartItems
from django.conf import settings
from custom_admin.models import DefaultSettings
from django.db.models import Count, F, Value, Subquery, DecimalField, Exists, ExpressionWrapper, FloatField, Sum
from django.db import transaction
from decimal import Decimal
from app_payment.tasks import handle_payment
from custom_admin.views import logger


class OrderView(View):

    @staticmethod
    def get(request):
        comment = OrderCommentForm()
        context = dict()
        context['comment'] = comment
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

            cart = CartItems.objects.filter(session_id=request.session.session_key, published=True).select_related(
                'product__discount').annotate(price_discount=ExpressionWrapper(
                F('price') * (1 - F('product__discount__discount_value') * Decimal('1.0') / 100),
                output_field=FloatField()), total_sum=Sum(F('price') * F('quantity')),
                total_sum_with_discount=Sum(F('price_discount') * F('quantity')))
            total_sum = 0
            total_sum_with_discount = 0
            for product in cart:
                total_sum += product.total_sum
                total_sum_with_discount += product.total_sum_with_discount
            context['cart'] = cart
            context['total_sum'] = total_sum
            context['total_sum_with_discount'] = total_sum_with_discount

            return render(request, template_name='order/order1.html', context=context)

    @staticmethod
    def post(request):
        comment = ''
        comment_form = OrderCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data.get('comment')
        data = request.POST
        print(data)
        email = data['mail']
        user = User.objects.get(email=email)
        delivery = Delivery.objects.get(title=data['delivery'])
        city = data['city']
        address = data['address']
        pay_method = PayMethod.objects.get(title=data['pay'])

        products = CartItems.objects.filter(session_id=request.session.session_key).select_related('product')
        order_goods = {}
        for product in products:
            order_goods[product.product_id] = product.quantity
        Order.objects.create(user=user, order_goods=order_goods, delivery=delivery, city=city,
                             address=address, pay_method=pay_method, order_comment=comment, payment_error='')

        if delivery.id == 1:
            return render(request, template_name='order/payment.html', )
        return render(request, template_name='order/payment_someone.html')


class OrderPayment(View):

    def post(self, request):
        card_num = request.POST['numero1']
        user = request.user
        profile = Profile.objects.get(user_id=user.id)
        order = Order.objects.filter(user=user).last()
        print(order.date_order)
        payment_amount = order.get_total_cost()
        if order.get_total_cost_with_discount():
            payment_amount = order.get_total_cost_with_discount()
        # handle_payment(order.id, card_num, payment_amount)
        return render(request, template_name='order/progressPayment.html')

    @transaction.atomic
    def get(self, request):
        user = request.user
        print('OK')
        profile = Profile.objects.get(user_id=user.id)
        # cart = CartItems.objects.filter(session_id=request.session.session_key).select_related('product')
        cart = CartItems.objects.filter(session_id=request.session.session_key, published=True).select_related(
            'product__discount').annotate(price_discount=ExpressionWrapper(
            F('price') * (1 - F('product__discount__discount_value') * Decimal('1.0') / 100),
            output_field=FloatField()), total_sum=Sum(F('price') * F('quantity')),
            total_sum_with_discount=Sum(F('price_discount') * F('quantity')))
        order = Order.objects.filter(user=user).last()

        if order.payment_error == 'оплачено':
            for product in cart:
                shop = Shop.objects.get(name=product.shop)
                shop_product = ShopProduct.objects.get(product=product.product, shop=shop.id)
                if shop_product.quantity - product.quantity >= 0:
                    shop_product.quantity -= product.quantity
                    shop_product.save()
                else:
                    logger.error(f'Заказ не оформлен. Недостаточное количество товара {product.product}')
                    order.payment_error = f'Недостаточное количество товара {product.product}'
                    return render(request, template_name='order/order_detail.html',
                                  context={'user': user,
                                           'profile': profile,
                                           'cart': cart,
                                           'order': order
                                           })
            logger.info(f'Оформление заказа пользователем {user.id} на сумму {order.get_total_cost()}руб.')
            for product in cart:
                product.published = False
                print(product.published)
            CartItems.objects.bulk_update(cart, ['published'])
            return render(request, template_name='cart.html')
        elif order.payment_error == 'не оплачено':
            logger.error(f'Заказ не оформлен. Ошибка оплаты')
            return render(request, template_name='order/order_detail.html', context={'user': user,
                                                                                     'profile': profile,
                                                                                     'cart': cart,
                                                                                     'order': order
                                                                                     })
        else:
            return render(request, template_name='order/progressPayment.html')




# return render(request, template_name='order/progressPayment.html')


# def handle_payment_test(order_id, card_num, payment_amount):
# 	return True

class OrderRepeat(View):

    def get(self, request):
        order = Order.objects.filter(user=request.user).last()
        if order.delivery_id == 1:
            return render(request, template_name='order/payment.html', )
        return render(request, template_name='order/payment_someone.html')
