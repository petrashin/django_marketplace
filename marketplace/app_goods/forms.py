from django import forms
from app_goods.models import Reviews


class ReviewForm(forms.ModelForm):
    """ Форма отзыва """

    class Meta:
        model = Reviews
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={"class": "form-textarea", "name": "review", "id": "review", "placeholder": "Review"}),
        }
