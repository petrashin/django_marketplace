from django import forms
# from django.utils.translation import gettext_lazy as _


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='количество', min_value=1, widget=forms.NumberInput )

class CartUpdateQuantityProductForm(forms.Form):
    quantity = forms.IntegerField(label='количество', min_value=1, widget=forms.NumberInput )
    item_id = forms.IntegerField(required=False, initial=False, widget=forms.HiddenInput)


class CartShopsForm(forms.Form):
    shop = forms.TypedChoiceField(
    choices = [],
    label='магазин',
    )




