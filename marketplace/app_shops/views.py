from django.views.generic import TemplateView


class ShopTemplateView(TemplateView):
    """ Вьюха для демонстрации магазина """
    template_name = 'shop.html'
