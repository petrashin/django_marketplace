from django.core.paginator import Paginator
from django.db.models import Avg, Max
from django.views.generic import TemplateView, DetailView, ListView
from app_goods.models import Category, Product
from app_shops.models import ShopProduct, Shop


class CatalogTemplateView(TemplateView):
    template_name = 'catalog.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data()
        page = self.request.GET.get('page', 1)
        products_qs = Product.objects.filter(category=kwargs["category_id"])
        products = Paginator(products_qs, 8).get_page(page)
        context['object_list'] = products
        return context


class BaseTemplateView(TemplateView):
    """ Вьюха для демонстрации базового шаблона """
    template_name = 'index.html'
    extra_context = {'title': "Megano"}


class ShopListView(ListView):
    context_object_name = 'products'
    template_name = 'shop_list.html'
    queryset = ShopProduct.objects.select_related('shop', 'product', 'price_type'). \
        filter(is_available=True). \
        prefetch_related('product__category', 'product__product_images')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = Category.objects.filter(parent_category__isnull=True).prefetch_related('products')
    #     print(context)
    #     return context


class ShopDetailView(DetailView):
    """ Детальная страница магазина """
    model = Shop
    context_object_name = 'shop'
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # товары магазина и средняя цена на них
        context['products'] = ShopProduct.objects. \
            filter(shop__slug=self.object.slug, is_available=True). \
            select_related('product', 'price_type'). \
            prefetch_related('product__product_images', 'product__category'). \
            values('product__name',
                   'product__slug',
                   'product__product_images__main_image',
                   'current_price',
                   'old_price',
                   'price_type__discount'
                   )
        # annotate(aver_price=Avg('current_price'),
        #          aver_old_price=Avg('old_price'),
        #          max_discount=Max('price_type__discount')
        #          )
        return context
