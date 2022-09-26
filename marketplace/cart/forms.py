from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CartItems


class CartAddProductForm(forms.Form):
    """Форма для добавления товара в корзину"""
    quantity = forms.IntegerField(label=_('quantity'), min_value=1,
    widget=forms.NumberInput(attrs={'style':'max-width: 5em'}))


class CartAddProductShopForm(forms.Form):
    """Форма для добавления товара выбранного магазина в корзину"""
    quantity = forms.IntegerField(min_value=1, widget=forms.HiddenInput)
    product = forms.IntegerField(required=False, widget=forms.HiddenInput)
    shop = forms.CharField(required=False, widget=forms.HiddenInput)


class CartUpdateQuantityProductForm(forms.Form):
    """Форма для обновления количества товара на странице корзины"""
    quantity = forms.IntegerField(label=_('quantity'), min_value=0,
    widget=forms.NumberInput(attrs={'style':'max-width: 5em'}) )
    item_id = forms.IntegerField(required=False, widget=forms.HiddenInput)


class CartShopsForm(forms.Form):
    """Форма для изменения магазина и цены товара на странице корзины"""
    def __init__(self, product, item_id, *args, **kwargs):
        self.product = product
        self.item_id = item_id
        super(CartShopsForm, self).__init__(*args, **kwargs)
        shops = CartItems().get_shops_for_cart_item(self.product)
        shop_tuple = tuple((shop.shop.id, shop.shop.name) for shop in shops)
        self.fields['shop'] = forms.ChoiceField(choices=shop_tuple, label='',
        widget=forms.Select(attrs={'style': 'min-height: 2em'}))
        self.fields['product'] = forms.IntegerField(required=False,
        widget=forms.HiddenInput,
        initial=self.product)
        self.fields['item_id'] = forms.IntegerField(required=False,
        widget=forms.HiddenInput,
        initial=self.item_id)
