from django.shortcuts import render, redirect
from django.views import View
from .forms import ProfileForm, DeliveryForm, PayMethodForm, OrderCommentForm
from .models import Order, Delivery, PayMethod
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from app_users.models import Profile
from app_goods.models import Product
from django.db import transaction
from cart.models import CartItems
from django.conf import settings


class OrderUserView(View):

    @staticmethod
    def get(request):
        titles = Delivery.objects.values_list('title', flat=True)
        if 'Доставка' not in titles:
            Delivery.objects.create(title='Доставка')
        if 'Экспресс-Доставка' not in titles:
            Delivery.objects.create(title='Экспресс-Доставка')
        pay_methods = PayMethod.objects.values_list('title', flat=True)
        if 'Онлайн картой' not in pay_methods:
            PayMethod.objects.create(title='Онлайн картой')
        if 'Онлайн со случайного чужого счёта' not in pay_methods:
            PayMethod.objects.create(title='Онлайн со случайного чужого счёта')

        user_form = ProfileForm()
        profile_form = ProfileForm()
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            user_form = ProfileForm(instance=user)
            profile = Profile.objects.filter(user_id=request.user.id)
            if profile:
                profile = Profile.objects.get(user_id=request.user.id)
            else:
                profile = Profile.objects.create(user=user, phone_number='')
            profile_form = ProfileForm(instance=profile)
        return render(request, template_name='order_user.html',
                      context={'user_form': user_form, 'profile_form': profile_form})

    @staticmethod
    def post(request):
        user_form = ProfileForm(request.POST)
        delivery_form = DeliveryForm()
        if request.user.is_authenticated:
            user = request.user
            profile = Profile.objects.get(user_id=user.id)
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                user.username = profile_form.cleaned_data.get('username')
                user.first_name = profile_form.cleaned_data.get('first_name')
                user.last_name = profile_form.cleaned_data.get('last_name')
                user.email = profile_form.cleaned_data.get('email')
                user.save()
                profile.phone_number = profile_form.cleaned_data.get('phone_number')
                profile.save()
            else:
                print(profile_form.errors)
                if profile_form.errors.get('phone_number'):
                    raise ValidationError('неверный номер телефона')
                else:
                    raise ValidationError('некорректные данные')
        else:
            if user_form.is_valid():
                if not user_form.cleaned_data.get('password_1') or not user_form.cleaned_data.get('password_2'):
                    raise ValidationError('введите пароли')
                elif user_form.cleaned_data.get('password_1') != user_form.cleaned_data.get('password_2'):
                    raise ValidationError('пароли не совпадают')
                else:
                    user = user_form.save()
                    password = user_form.cleaned_data.get('password_1')
                    user.set_password(password)
                    user.save()
                    user = authenticate(username=user.username, password=password)
                    login(request, user)
                    phone_number = user_form.cleaned_data.get('phone_number')
                    Profile.objects.create(user=user, phone_number=phone_number)
            else:
                if user_form.errors.get('username'):
                    raise ValidationError('имя пользователя уже существует')
                elif user_form.errors.get('email'):
                    raise ValidationError('email уже существует')
                elif user_form.errors.get('phone_number'):
                    raise ValidationError('неверный номер телефона')
                else:
                    raise ValidationError('некорректные данные')
        return render(request, template_name='order_delivery.html', context={'delivery_form': delivery_form})


class OrderDeliveryView(View):

    @staticmethod
    def post(request):
        pay_method_form = PayMethodForm()
        delivery_form = DeliveryForm(request.POST)
        user = User.objects.get(id=request.user.id)
        print(delivery_form.errors)
        if delivery_form.is_valid():
            id_delivery = delivery_form.cleaned_data.get('title')
            city = delivery_form.cleaned_data.get('city')
            address = delivery_form.cleaned_data.get('address')
            delivery = Delivery.objects.get(id=id_delivery)
            Order.objects.create(user=user, delivery=delivery, city=city, address=address)
            return render(request, template_name='order_pay_method.html', context={'pay_method_form': pay_method_form})


class OrderPayMethodView(View):

    @staticmethod
    def post(request):
        order_comment = OrderCommentForm()
        pay_method_form = PayMethodForm(request.POST)
        order = Order.objects.filter(user=request.user).order_by('-id')[0]
        if pay_method_form.is_valid():
            id_pay_method = pay_method_form.cleaned_data.get('title')
            pay_metod = PayMethod.objects.get(id=id_pay_method)
            order.pay_method = pay_metod
            order.save()

        order_delivery_pay = 0
        if order.delivery.title == 'Экспресс-Доставка':
            order_delivery_pay = 500
        elif order_total_sum < 2000:
            order_delivery_pay = 200

        order_cart = request.session[settings.CART_SESSION_ID]

        products = Product.objects.filter(id__in=order_cart.keys())
        print(products[0].description)
        # for id_product in order_cart.keys():
        # 	product = Product.objects.filter(id=id_product)
        # 	products.append(product)
        #
        # 	quantity = order_cart[id_product]['quantity']
        # 	price = order_cart[id_product]['price']
        #
        #
        # print(products)
        return render(request, template_name='order_total.html', context={'order': order, 'products': products,
                                                                          'order_delivery_pay': order_delivery_pay,
                                                                          'order_comment': order_comment})


class OrderTotal(View):

    @staticmethod
    def post(request):
        order_comment = OrderCommentForm(request.POST)
        if order_comment.is_valid():
            order = Order.objects.filter(user=request.user).order_by('-id')[0]
            order_comment = order_comment.cleaned_data.get('order_comment')
            order.order_comment = order_comment
            order.save()

        service_payment()
        return redirect('/')


@transaction.atomic
def service_payment():
    pass
