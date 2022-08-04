from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, TemplateView

from app_goods.models import Product, Reviews
from app_goods.forms import ReviewForm
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
    extra_context = {'title': 'Товар', 'review_form': ReviewForm, 'reviews': Reviews.objects.all}


class AddReview(View):
    """ Отзыв """

    def post(self, request, slug):
        form = ReviewForm(request.POST)
        product = Product.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            user = User.objects.get(id=request.user.id)
            form.user = user
            form.email = user.email
            form.product = product

            form.save()

        return redirect(product.get_absolute_url())
