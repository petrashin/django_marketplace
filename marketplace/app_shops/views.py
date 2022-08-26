from django.core.paginator import Paginator
from django.db.models import Count, F
from django.views.generic import TemplateView, DetailView, ListView
from app_shops.models import ShopProduct, Shop
from cart.forms import CartAddProductShopForm

SORT_OPTIONS = {
    'price': F('price'),
    'new': F('product__created_at'),
    'reviews': Count('product__reviews'),
    'popularity': F('product__views_count'),
}

SORT_DIRECTIONS = {
    'ascending': '-',
    'descending': '',
}

DEFAULT_OPTION = F('id')
DEFAULT_DIRECTION = ''


class CatalogTemplateView(TemplateView):
    template_name = 'catalog.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data()

        get_sort_key = self.request.GET.get('sort', DEFAULT_OPTION)
        get_sort_direction = self.request.GET.get('type', DEFAULT_DIRECTION)
        sort_key = SORT_OPTIONS.get(get_sort_key, DEFAULT_OPTION)
        sort_direction = SORT_DIRECTIONS.get(get_sort_direction, DEFAULT_DIRECTION)

        products_qs = ShopProduct.objects.filter(product__category=kwargs["category_id"]). \
            annotate(count=sort_key).order_by(sort_direction + 'count')
        page = self.request.GET.get('page', 1)
        products = Paginator(products_qs, 8).get_page(page)
        context['object_list'] = products
        return context


class BaseTemplateView(TemplateView):
    """ Вьюха для демонстрации базового шаблона """
    template_name = 'index.html'
    extra_context = {'title': "Megano"}


class ShopListView(ListView):
    context_object_name = 'products'
    template_name = 'app_shops/shop_list.html'
    queryset = ShopProduct.objects.select_related('shop', 'product'). \
        filter(is_available=True). \
        prefetch_related('product__category', 'product__product_images')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in self.object_list:
            product.add_to_cart_form = CartAddProductShopForm(initial={'quantity': 1,
                                                                       'shop': product.shop.name,
                                                                       'product': product.product.id
                                                                       })
        return context


class ShopDetailView(DetailView):
    """ Детальная страница магазина """
    model = Shop
    context_object_name = 'shop'
    template_name = 'app_shops/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # товары магазина
        context['products'] = ShopProduct.objects. \
            filter(shop__slug=self.object.slug, is_available=True). \
            select_related('product'). \
            prefetch_related('product__product_images', 'product__category')
        if context['products']:
            if len(context['products']) > 1:
                for product in context['products']:
                    product.add_to_cart_form = CartAddProductShopForm(initial={'quantity': 1,
                                                                               'shop': self.object.name,
                                                                               'product': product.product.id
                                                                               })
            else:
                product = context['products'][0]
                product.add_to_cart_form = CartAddProductShopForm(initial={'quantity': 1,
                                                                           'shop': self.object.name,
                                                                           'product': product.product.id
                                                                           })

        return context

