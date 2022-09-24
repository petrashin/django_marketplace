from django import forms
from django.contrib.auth.models import User
from app_users.models import Profile
from .models import Delivery, PayMethod


class OrderCommentForm(forms.Form):
	
	order_comment = forms.CharField(required=False, help_text='комментарий к заказу')
