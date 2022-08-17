from django import forms
# from django.utils.translation import gettext_lazy as _
from .models import CartItems



class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='количество', min_value=1, widget=forms.NumberInput )

class CartUpdateQuantityProductForm(forms.Form):
    quantity = forms.IntegerField(label='количество', min_value=1, widget=forms.NumberInput )
    item_id = forms.IntegerField(required=False, widget=forms.HiddenInput)


class CartShopsForm(forms.Form):
    options = CartItems().get_shops_for_cart_item(product=None)
    shop = forms.ChoiceField(
    choices = options,
    label='магазин',
    )
    item_id = forms.IntegerField(required=False, widget=forms.HiddenInput)




