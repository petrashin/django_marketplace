import django_filters
from django import forms
from app_shops.models import Shop


class ProductFilter(django_filters.FilterSet):

    product__name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={
                'class': "form-input form-input_full",
                'placeholder': "Название"
            }
        )
    )
    shop = django_filters.ModelChoiceFilter(
        queryset=Shop.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        empty_label="Продавец"
    )
    is_available = django_filters.BooleanFilter(
        widget=forms.CheckboxInput,
        method='indeterminate_checkbox',
    )
    price = django_filters.CharFilter(
        method='price_range',
        widget=forms.TextInput(
            attrs={
                'class': 'range-line',
                'data-type': 'double',
                'data-min': '0',
                'data-max': '2000',
            }
        )
    )

    @staticmethod
    def indeterminate_checkbox(queryset, _, value):
        if not value:
            return queryset.all()
        return queryset.filter(is_available=True)

    @staticmethod
    def price_range(queryset, _, value):
        queryset = queryset.filter(price__range=value.split(';'))
        return queryset
