from django import forms
from django.contrib.auth.models import User
from .models import DefaultSettings


class ImportGoodsForm(forms.Form):
	file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class EmailForReportImport(forms.ModelForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ['email']


class DefaultSettingsForm(forms.ModelForm):
	
	delivery_express_coast = forms.IntegerField(help_text='Стоимость экспресс доставки')
	min_order = forms.IntegerField(help_text='Минимальная стоимость заказа')
	delivery_min = forms.IntegerField(help_text='Стоимость доставки при стоимости заказа меньше минимальной')

	class Meta:
		model = DefaultSettings
		fields = ['delivery_express_coast', 'min_order', 'delivery_min']
