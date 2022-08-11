from django.views.generic import TemplateView
from django.core.paginator import Paginator
from app_goods.models import Product


class ShopTemplateView(TemplateView):
    """ Вьюха для демонстрации магазина """
    template_name = 'shop.html'


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
