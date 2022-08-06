from django.views.generic import TemplateView
from app_goods.models import Category


class ShopTemplateView(TemplateView):
    """ Вьюха для демонстрации магазина """
    template_name = 'shop.html'


class CatalogTemplateView(TemplateView):
    template_name = 'catalog.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data()
        context['categories'] = Category.objects.filter(parent_category__isnull=True)
        return context


class BaseTemplateView(TemplateView):
    """ Вьюха для демонстрации базового шаблона """
    template_name = 'index.html'
    extra_context = {'title': "Megano"}

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data()
        context['categories'] = Category.objects.filter(parent_category__isnull=True)
        return context
