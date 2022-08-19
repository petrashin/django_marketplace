from django import forms
from django.contrib.auth.models import User
from app_users.models import Profile
from .models import Delivery, PayMethod


class ProfileForm(forms.ModelForm):
	username = forms.CharField(max_length=30, help_text='Ник')
	first_name = forms.CharField(max_length=30, help_text='Имя')
	last_name = forms.CharField(max_length=30, help_text='Фамилия')
	email = forms.CharField(max_length=30, help_text='email')
	phone_number = forms.CharField(max_length=30, help_text='Номер телефона')
	password_1 = forms.CharField(max_length=30, required=False, help_text='Пароль')
	password_2 = forms.CharField(max_length=30, required=False, help_text='Подтверждение пароля')

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']


class DeliveryForm(forms.ModelForm):
	
	delivery = forms.ChoiceField(initial=1, required=False, help_text='вариант доставки')
	city = forms.CharField(help_text='город')
	address = forms.CharField(help_text='адрес доставки')
	
	class Meta:
		model = Delivery
		fields = ['title', 'city', 'address']
		

class PayMethodForm(forms.ModelForm):
	
	pay_method = forms.ChoiceField(initial=1, required=False, help_text='вариант оплаты')
	
	class Meta:
		model = PayMethod
		fields = ['title']


class OrderCommentForm(forms.Form):
	
	order_comment = forms.CharField(required=False, help_text='комментарий к заказу')
