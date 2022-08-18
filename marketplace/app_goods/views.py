from django.contrib.auth.models import User
from django.db.models import Avg, Max, IntegerField
from django.shortcuts import redirect
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView

from app_goods.models import Product, Reviews
from app_shops.models import ShopProduct
from app_goods.forms import ReviewForm
from cart.forms import CartAddProductForm


# class ProductsListView(ListView):
#     model = Product
#     context_object_name = 'goods'
#     queryset = Product.objects.prefetch_related('product_images').all()
#     template_name = 'shop.html'

class ProductDetailView(FormMixin, DetailView):
    """ Представление для получения детальной информации о продукте
    и добавления его в корзину"""
    model = Product
    context_object_name = 'product'
    template_name = 'product.html'
    form_class = CartAddProductForm
    extra_context = {'title': 'Товар', 'review_form': ReviewForm, 'reviews': Reviews.objects.all}

    def get_object(self, *args, **kwargs):
        view_object = super(ProductDetailView, self).get_object()
        view_object.views_count += 1
        view_object.save()
        return view_object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # считаем среднюю цену товара по магазинам без скидки и со скидкой и максимальную скидку в %
        # и добавляем в контекст
        context['aver_price'] = ShopProduct.objects.filter(product=self.object.id). \
            aggregate(discounted_price=Avg('current_price', output_field=IntegerField()),
                      base_price=Avg('old_price', output_field=IntegerField()),
                      discount=Max('price_type__discount')
                      )
        # добавляем в контекст магазины и цену товара в них
        context['shops'] = ShopProduct.objects.filter(product=self.object.id). \
            select_related('shop', 'product', 'price_type'). \
            values('shop__name', 'current_price', 'quantity')
        return context


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
