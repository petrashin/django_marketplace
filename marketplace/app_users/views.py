from django.views.generic import TemplateView


from app_goods.models import Product, Category


class BaseTemplateView(TemplateView):
    """ Вьюха для демонстрации базового шаблона """
    template_name = 'index.html'
    extra_context = {'title': "Megano"}

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data()
        context['categories'] = Category.objects.filter(parent_category__isnull=True)
        products = Product.objects.all().order_by('-views_count')
        context['top_goods'] = products[:4]
        context['top_goods_hide_md'] = products[4:6]
        context['top_goods_hide_1450'] = products[6:8]
        return context
