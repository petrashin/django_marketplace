from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_goods.models import Category, Product


class ShopTemplateView(TemplateView):
    """ Вьюха для демонстрации магазина """
    template_name = 'shop.html'


class CatalogTemplateView(TemplateView):
    template_name = 'catalog.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data()
        context['categories'] = Category.objects.filter(parent_category__isnull=True)
        products_list = Product.objects.filter(category=kwargs["category_id"])
        paginator = Paginator(products_list, 8)
        if 'page' in self.request.GET:
            page = self.request.GET['page']
        else:
            page = 1
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context['object_list'] = products
        return context


class BaseTemplateView(TemplateView):
    """ Вьюха для демонстрации базового шаблона """
    template_name = 'index.html'
    extra_context = {'title': "Megano"}

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data()
        context['categories'] = Category.objects.filter(parent_category__isnull=True)
        return context
