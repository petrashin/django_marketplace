from statistics import mean

from django.shortcuts import render
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView

from app_users.models import ViewsHistory, ComparedProducts, Role, Image
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
        product = Product.objects.get(id=self.object.id)

        # добавление товара в историю просмотра
        if self.request.user.is_authenticated:
            if Profile.objects.filter(user_id=self.request.user.id).exists():
                profile = Profile.objects.get(user_id=self.request.user.id)
                ViewsHistory.objects.create(profile=profile, product=product)

        # добавляем в контекст магазины, которые продают этот товар и активируем кнопку добавления в корзину
        shops = ShopProduct.objects.filter(product=self.object.id).select_related('shop', 'product')
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


class CompareGoodsView(View):
    """Вьюшка сравнения товаров"""

    def can_be_compared(self, lst):
        lst_of_specs = [el.keys() for el in lst]
        return len(set(lst_of_specs[0]).intersection(*lst_of_specs)) != 0

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
                    all_specs[k] = [''] * len(lst_of_tech_specs)
                all_specs[k][i] = v

        for k, v in all_specs.items():
            if not self.check_same_elements(all_specs[k]):
                diff_specs[k] = v

        for k, v in all_specs.items():
            if len(set(v)) == 1:
                same_specs[k] = v

        return all_specs, diff_specs, same_specs

    def get(self, request):

        if request.user.is_anonymous:
            data = {}
        else:
            if request.user.is_superuser and not Profile.objects.filter(user_id=request.user.id).exists():
                role = Role.objects.get_or_create(name='Администратор')[0]
                profile = Profile.objects.create(user=request.user, role=role)
                Image.objects.create(profile=profile)
            else:
                profile = Profile.objects.get(user=request.user)

            compared_products = ComparedProducts.objects.filter(profile=profile)
            products = []
            tech_specs = []
            not_enough_data = False

            if len(compared_products) != 0:

                for obj in compared_products:
                    product = Product.objects.get(pk=obj.product.id)
                    products.append(product)
                    tech_specs.append(product.technical_specs)

                if len(tech_specs) < 2:
                    not_enough_data = True
                    all_specs, diff_specs, same_specs = {}, {}, {}
                else:
                    all_specs, diff_specs, same_specs = self.parse_technical_specs(tech_specs)

                can_compare = self.can_be_compared(tech_specs)

                data = {
                    'can_compare': can_compare,
                    'same_specs': same_specs,
                    'all_specs': all_specs,
                    'diff_specs': diff_specs,
                    'not_enough_data': not_enough_data,
                    'compared_products': products
                }

            else:
                data = {
                    'not_enough_data': True
                }

        return render(request, 'app_goods/compare.html', context=data)


def delete_from_comparison(request, pk):
    """Функция для удаления товара из меню сравнения"""
    profile = Profile.objects.get(user=request.user)
    ComparedProducts.objects.get(profile=profile, product=pk).delete()
    return redirect('compare')


def add_to_comparison(request, pk):
    """
    Функция для добавления товара в меню сравнения
    При добавлении пятого товара в сравнение удаляет первый добавленный товар
    """
    profile = Profile.objects.get(user=request.user)
    if not ComparedProducts.objects.filter(profile=profile, product_id=pk).exists():
        if ComparedProducts.objects.filter(profile=profile).count() > 3:
            ComparedProducts.objects.filter(profile=profile).order_by('added_at').first().delete()
        ComparedProducts.objects.create(profile=profile, product_id=pk)

    return redirect('compare')
