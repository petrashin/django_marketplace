from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView

from app_users.models import ViewsHistory
from app_goods.models import Product, Reviews
from app_shops.models import ShopProduct
from app_goods.forms import ReviewForm
from cart.forms import CartAddProductForm, CartAddProductShopForm
from app_users.models import Profile

from app_shops.views import AddToCartFormMixin


class ProductDetailView(FormMixin, AddToCartFormMixin, DetailView):
    """ Представление для получения детальной информации о продукте
    и добавления его в корзину"""
    model = Product
    context_object_name = 'product'
    template_name = 'app_goods/product.html'
    form_class = CartAddProductForm
    extra_context = {'title': _('Product'), 'review_form': ReviewForm, 'reviews': Reviews.objects.all}

    def get_object(self, *args, **kwargs):
        view_object = super(ProductDetailView, self).get_object()
        view_object.views_count += 1
        view_object.save()
        return view_object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # добавление товара в историю просмотра
        profile = Profile.objects.filter(user_id=self.request.user.id).get()
        product = Product.objects.get(id=self.object.id)
        ViewsHistory.objects.create(profile=profile, product=product)

        # считаем среднюю цену товара по магазинам без скидки и со скидкой и добавляем в контекст
        shops = ShopProduct.objects.filter(product=self.object.id).select_related('shop', 'product')
        context['price'] = product.get_avg_price()
        context['discounted_aver_price'] = product.get_avg_discounted_price()
        context['shops'] = shops

        self.add_to_cart_form(shops)

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


