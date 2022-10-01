import math
import random

from django.core.paginator import Paginator
from django.db.models import Count, F, Avg, Case, When, DecimalField, Max, Min
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, DetailView, ListView

from app_goods.models import ProductTag
from app_shops.filters import ProductFilter
from app_shops.models import ShopProduct, Shop, Product
from cart.forms import CartAddProductShopForm


SORT_OPTIONS = {
    'price': Avg('shop_products__price') * Case(
        When(discount__discount_value__isnull=False, then=1 - (F('discount__discount_value') * 0.01)),
        default=1,
        output_field=DecimalField(),
    ),
    'new': F('created_at'),
    'reviews': Count('reviews'),
    'popularity': F('views_count'),
}

SORT_DIRECTIONS = {
    'ascending': '',
    'descending': '-',
}

DEFAULT_OPTION = F('id')
DEFAULT_DIRECTION = ''


class AddToCartFormMixin:
    """ Миксин для активации кнопки добавления товара в корзину на карточках товаров """

    def get_form_params(self, object):
        if not hasattr(object, 'shop'):
            shop = None
        else:
            shop = object.shop.slug
        if not hasattr(object, 'product'):
            product_id = object.id
        else:
            product_id = object.product.id
        return [shop, product_id]

    def add_to_cart_form(self, products):
        if products:
            if len(products) > 1:
                for product in products:
                    shop = self.get_form_params(product)[0]
                    product_id = self.get_form_params(product)[1]
                    product.add_to_cart_form = CartAddProductShopForm(initial={'quantity': 1,
                                                                               'shop': shop,
                                                                               'product': product_id
                                                                               })
            else:
                shop = self.get_form_params(products[0])[0]
                product_id = self.get_form_params(products[0])[1]
                products[0].add_to_cart_form = CartAddProductShopForm(initial={'quantity': 1,
                                                                               'shop': shop,
                                                                               'product': product_id
                                                                               })


class CatalogueView(AddToCartFormMixin, ListView):
    template_name = 'catalog.html'

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs["category_id"])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CatalogueView, self).get_context_data()
        page = self.request.GET.get('page', 1)
        tag = self.request.GET.get('tag', None)
        get_sort_key = self.request.GET.get('sort', DEFAULT_OPTION)
        get_sort_direction = self.request.GET.get('type', DEFAULT_DIRECTION)
        sort_key = SORT_OPTIONS.get(get_sort_key, DEFAULT_OPTION)
        sort_direction = SORT_DIRECTIONS.get(get_sort_direction, DEFAULT_DIRECTION)
        f = ProductFilter(self.request.GET, queryset=self.get_queryset())
        sorted_qs = f.qs.annotate(count=sort_key).order_by(sort_direction + 'count')
        if tag:
            sorted_qs = sorted_qs.filter(tags__tag=tag)
        products = Paginator(sorted_qs, 8).get_page(page)
        context['filter'] = f
        context['products'] = products
        context['tags'] = ProductTag.objects.all()[:6:]
        context['max_price'] = math.ceil(sorted_qs.annotate(
            avg_price=SORT_OPTIONS['price']).aggregate(Max('avg_price'))['avg_price__max'])
        context['min_price'] = math.floor(sorted_qs.annotate(
            avg_price=SORT_OPTIONS['price']).aggregate(Min('avg_price'))['avg_price__min'])

        self.add_to_cart_form(products)

        return context


class BaseTemplateView(AddToCartFormMixin, TemplateView):
    """ Вьюха для демонстрации базового шаблона """
    template_name = 'index.html'
    extra_context = {'title': _("Megano")}

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data()
        products = Product.objects.filter(published=True)
        popular_products = products.order_by('-sales_count')[:8]
        limited_products = products.filter(limited_edition=True)
        hot_offers = products.filter(discount__discount_value__gt=0)[:9]
        self.add_to_cart_form(popular_products)
        self.add_to_cart_form(limited_products)
        self.add_to_cart_form(hot_offers)
        if limited_products:
            if len(limited_products) > 1:
                context['lim_products'] = limited_products[:16]
            else:
                context['lim_products'] = limited_products[0]

        context['popular_products'] = popular_products
        context['hot_offers'] = hot_offers
        return context


class ShopListView(AddToCartFormMixin, ListView):
    context_object_name = 'products'
    template_name = 'app_shops/shop_list.html'
    queryset = ShopProduct.objects.select_related('shop', 'product'). \
        filter(product__published=True). \
        prefetch_related('product__category', 'product__product_images').order_by('shop__name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.object_list
        self.add_to_cart_form(products)
        return context


class ShopDetailView(AddToCartFormMixin, DetailView):
    """ Детальная страница магазина """
    model = Shop
    context_object_name = 'shop'
    template_name = 'app_shops/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # товары магазина
        products = ShopProduct.objects. \
                       filter(shop__slug=self.object.slug, product__published=True). \
                       select_related('product'). \
                       prefetch_related('product__category', 'product__product_images'). \
                       order_by('-product__sales_count')[:10]
        context['products'] = products
        self.add_to_cart_form(products)
        return context

