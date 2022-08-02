from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, TemplateView

from app_goods.models import Product
from cart.forms import CartAddProductForm


class ProductsListView(ListView):
    model = Product
    context_object_name = 'goods'
    queryset = Product.objects.prefetch_related('product_images').all()
    template_name = 'shop.html'


class ProductDetailView(FormMixin, DetailView):
    """ Представление для получения детальной информации о продукте
    и добавления его в корзину"""
    model = Product
    context_object_name = 'product'
    template_name = 'product.html'
    form_class = CartAddProductForm
    extra_context = {'title': 'Товар'}

