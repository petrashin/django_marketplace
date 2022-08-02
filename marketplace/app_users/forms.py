from django import forms
from app_users.models import Reviews


class ReviewForm(forms.ModelForm):
    """ Форма отзыва """

    class Meta:
        model = Reviews
        fields = ('product', 'text')
        widgets = {
            'product': forms.TextInput(),
            'text': forms.Textarea(),
        }
