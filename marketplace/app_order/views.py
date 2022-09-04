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


class OrderView(View):

    @staticmethod
    def get(request):
        comment = OrderCommentForm()
        context = dict()
        context['comment'] = comment
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            context['user'] = user
            cart = CartItems.objects.filter(session_id=request.session.session_key).select_related('product')
            context['cart'] = cart
            profile = Profile.objects.filter(user_id=request.user.id)
            if profile:
                profile = Profile.objects.get(user_id=request.user.id)
            else:
                profile = Profile.objects.create(user=user, phone_number='')
            context['profile'] = profile
            total_sum = 0
            total_sum_with_discount = 0
            for product in cart:
                shop_id = Shop.objects.get(name=product.shop).id
                shop_product = ShopProduct.objects.get(shop=shop_id, product=product.product)
                total_sum += product.price * product.quantity
                total_sum_with_discount += shop_product.get_discounted_price() * product.quantity
            context['total_sum'] = total_sum
            context['total_sum_with_discount'] = total_sum_with_discount
            return render(request, template_name='order.html', context=context)

    @staticmethod
    def post(request):
        comment = ''
        comment_form = OrderCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data.get('comment')
        data = request.POST
        email = data['mail']
        user = User.objects.get(email=email)
        delivery = Delivery.objects.get(title=data['delivery'])
        city = data['city']
        address = data['address']
        pay_method = PayMethod.objects.get(title=data['pay'])
        
        cart = CartItems.objects.filter(user=user.id).last()
        products = CartItems.objects.filter(session_id=request.session.session_key).select_related('product')
        order_goods = {}
        for product in products:
            order_goods[product.product_id] = product.quantity
        Order.objects.create(user=user, cart=cart, order_goods=order_goods, delivery=delivery, city=city,
                             address=address, pay_method=pay_method, order_comment=comment, payment_error='')
        if delivery.id == 1:
            return render(request, template_name='payment.html', )
        return render(request, template_name='payment_someone.html')
    
    
class OrderPayment(View):
    
    @staticmethod
    def post(request):
        card_number = request.POST['numero1']
        return render(request, template_name='progressPayment.html')

#         if request.user.is_authenticated:
#             user = request.user
#             profile = Profile.objects.get(user_id=user.id)
#             profile_form = ProfileForm(request.POST, instance=profile)
#             if profile_form.is_valid():
#                 user.username = profile_form.cleaned_data.get('username')
#                 user.first_name = profile_form.cleaned_data.get('first_name')
#                 user.last_name = profile_form.cleaned_data.get('last_name')
#                 user.email = profile_form.cleaned_data.get('email')
#                 user.save()
#                 profile.phone_number = profile_form.cleaned_data.get('phone_number')
#                 profile.save()
#             else:
#                 print(profile_form.errors)
#                 if profile_form.errors.get('phone_number'):
#                     raise ValidationError('неверный номер телефона')
#                 else:
#                     raise ValidationError('некорректные данные')
#         else:
#             if user_form.is_valid():
#                 if not user_form.cleaned_data.get('password_1') or not user_form.cleaned_data.get('password_2'):
#                     raise ValidationError('введите пароли')
#                 elif user_form.cleaned_data.get('password_1') != user_form.cleaned_data.get('password_2'):
#                     raise ValidationError('пароли не совпадают')
#                 else:
#                     user = user_form.save()
#                     password = user_form.cleaned_data.get('password_1')
#                     user.set_password(password)
#                     user.save()
#                     user = authenticate(username=user.username, password=password)
#                     login(request, user)
#                     phone_number = user_form.cleaned_data.get('phone_number')
#                     Profile.objects.create(user=user, phone_number=phone_number)
#             else:
#                 if user_form.errors.get('username'):
#                     raise ValidationError('имя пользователя уже существует')
#                 elif user_form.errors.get('email'):
#                     raise ValidationError('email уже существует')
#                 elif user_form.errors.get('phone_number'):
#                     raise ValidationError('неверный номер телефона')
#                 else:
#                     raise ValidationError('некорректные данные')
#         return render(request, template_name='order_delivery.html', context={'delivery_form': delivery_form})
#
#         order_delivery_pay = 0
#         if order.delivery.title == 'Экспресс-Доставка':
#             order_delivery_pay = 500
#         elif order_total_sum < 2000:
#             order_delivery_pay = 200
