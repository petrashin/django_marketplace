from django import forms


class OrderCommentForm(forms.Form):
	
	order_comment = forms.CharField(required=False, help_text='комментарий к заказу')
