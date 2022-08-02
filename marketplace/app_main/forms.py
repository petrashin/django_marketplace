from django import forms
from app_main.models import Reviews


class ReviewForm(forms.ModelForm):
    """ Форма отзыва """

    class Meta:
        model = Reviews
        fields = ('product', 'text')
        widgets = {
            'product': forms.TextInput(),
            'text': forms.Textarea(),
        }
