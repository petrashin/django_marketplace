from statistics import mean

from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView

from app_users.models import ViewsHistory, ComparedProducts, Role, Image
from app_goods.models import Product, Reviews
from app_shops.models import ShopProduct
from app_goods.forms import ReviewForm
from cart.forms import CartAddProductForm, CartAddProductShopForm
from app_users.models import Profile


class ProductDetailView(FormMixin, DetailView):
    """ Представление для получения детальной информации о продукте
    и добавления его в корзину"""
    model = Product
    context_object_name = 'product'
    template_name = 'app_goods/product.html'
    form_class = CartAddProductForm
    extra_context = {'title': 'Товар', 'review_form': ReviewForm, 'reviews': Reviews.objects.all}

    def get_object(self, *args, **kwargs):
        view_object = super(ProductDetailView, self).get_object()
        view_object.views_count += 1
        view_object.save()
        return view_object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # добавление товара в историю просмотра
        profile = Profile.objects.get(user_id=self.request.user.id)
        product = Product.objects.get(id=self.object.id)
        ViewsHistory.objects.create(profile=profile, product=product)

        # считаем среднюю цену товара по магазинам без скидки и со скидкой и добавляем в контекст
        products = ShopProduct.objects.filter(product=self.object.id).select_related('shop', 'product')
        context['price'] = product.get_avg_price()
        context['discounted_aver_price'] = round(mean([product.get_discounted_price() for product in products]), 2)
        context['shops'] = products
        if context['shops']:
            if len(context['shops']) > 1:
                for shop in context['shops']:
                    shop.add_to_cart_form = CartAddProductShopForm(initial={'quantity': 1,
                                                                            'shop': shop.shop.name,
                                                                            'product': self.object.id
                                                                            })
            else:
                shop = context['shops'][0]
                shop.add_to_cart_form = CartAddProductShopForm(initial={'quantity': 1,
                                                                        'shop': shop.shop.name,
                                                                        'product': self.object.id
                                                                        })
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


class CompareGoodsView(View):
    """Вьюшка сравнения товаров"""

    def check_same_elements(self, lst):
        if len(lst) == 2:
            return lst[0] == lst[1]
        elif len(lst) == 3:
            return lst[0] == lst[1] == lst[2]
        elif len(lst) == 4:
            return lst[0] == lst[1] == lst[2] == lst[3]
        else:
            return BaseException

    def parse_technical_specs(self, lst_of_tech_specs):
        """
        Возвращает три словаря:
            первый - все характеристики товаров,
            второй - только различающиеся характеристики товаров,
            третий - только одинаковые характеристики товаров
        """
        all_specs = {}
        diff_specs = {}
        same_specs = {}

        for i in range(len(lst_of_tech_specs)):
            for k, v in lst_of_tech_specs[i].items():
                if k not in all_specs:
                    all_specs[k] = [''] * 4
                all_specs[k][i] = v

        for k, v in all_specs.items():
            if not self.check_same_elements(all_specs[k]):
                diff_specs[k] = v

        for k, v in all_specs.items():
            if k not in diff_specs:
                same_specs[k] = v

        return all_specs, diff_specs, same_specs

    def get(self, request):

        if request.user.is_superuser and not Profile.objects.filter(user_id=request.user.id).exists():
            role = Role.objects.get_or_create(name='Администратор')[0]
            profile = Profile.objects.create(user=request.user, role=role)
            Image.objects.create(profile=profile)
        else:
            profile = Profile.objects.get(user=request.user)

        products = []
        tech_specs = []
        not_enough_data = False

        for obj in ComparedProducts.objects.filter(profile=profile):
            product = Product.objects.get(pk=obj.product.id)
            products.append(product)
            tech_specs.append(product.technical_specs)

        if len(tech_specs) < 2:
            not_enough_data = True
            all_specs, diff_specs, same_specs = {}, {}, {}
        else:
            all_specs, diff_specs, same_specs = self.parse_technical_specs(tech_specs)

        data = {
            'same_specs': same_specs,
            'all_specs': all_specs,
            'diff_specs': diff_specs,
            'not_enough_data': not_enough_data,
            'compared_products': products
        }

        return render(request, 'app_goods/compare.html', context=data)
