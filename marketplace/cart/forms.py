from django import forms
# from django.utils.translation import gettext_lazy as _
from .models import CartItems



class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='количество', min_value=1, widget=forms.NumberInput )

class CartUpdateQuantityProductForm(forms.Form):
    quantity = forms.IntegerField(label='количество', min_value=1, widget=forms.NumberInput )
    item_id = forms.IntegerField(required=False, widget=forms.HiddenInput)


class CartShopsForm(forms.Form):
    def __init__(self, product, item_id, *args, **kwargs):
        self.product = product
        self.item_id = item_id
        super(CartShopsForm, self).__init__(*args, **kwargs)
        shops = CartItems().get_shops_for_cart_item(self.product)
        shop_tuple = tuple((shop.shop.id, shop.shop.name) for shop in shops)
        self.fields['shop'] = forms.ChoiceField(choices=shop_tuple, label='магазин')
        self.fields['product'] = forms.IntegerField(required=False,
        widget=forms.HiddenInput,
        initial=self.product)
        self.fields['item_id'] = forms.IntegerField(required=False,
        widget=forms.HiddenInput,
        initial=self.item_id)

#shops = CartItems().get_shops_for_cart_item(product=1)
#shop_tuple = tuple((str(shop.get_discounted_price()), shop.shop.name) for shop in shops)
#print(shop_tuple)
print(CartShopsForm(product=2, item_id=32).as_p())
