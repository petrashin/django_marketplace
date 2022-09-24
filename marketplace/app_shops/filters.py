import django_filters
from django import forms
from django.db.models import Avg, When, Case, F, DecimalField

from django.utils.translation import gettext_lazy as _
from app_shops.models import Shop


class ProductFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={
                'class': "form-input form-input_full",
                'placeholder': _("Title")
            }
        )
    )
    price = django_filters.CharFilter(
        method='price_range',
        widget=forms.TextInput(
            attrs={
                'class': 'range-line',
                'data-type': 'double',
                'data-min': '0',
                'data-max': '20000',
            }
        )
    )
    shop = django_filters.ModelChoiceFilter(
        method='filter_by_shop',
        queryset=Shop.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        empty_label=_("Seller")
    )
    published = django_filters.BooleanFilter(
        widget=forms.CheckboxInput,
        method='indeterminate_checkbox',
    )

    @staticmethod
    def indeterminate_checkbox(queryset, _, value):
        if not value:
            return queryset.all()
        return queryset.filter(published=True)

    @staticmethod
    def price_range(queryset, _, value):
        queryset = queryset.annotate(
            disc_price=Avg('shop_products__price') * Case(
                When(discount__discount_value__isnull=False, then=1 - (F('discount__discount_value') * 0.01)),
                default=1,
                output_field=DecimalField(),
            )
        ).filter(disc_price__range=value.split(';'))
        return queryset

    @staticmethod
    def filter_by_shop(queryset, _, value):
        queryset = queryset.filter(shop_products__shop=value)
        return queryset
