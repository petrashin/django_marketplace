import decimal

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from app_goods.models import Product
from app_shops.models import ShopProduct, Shop
from .forms import CartAddProductForm, CartShopsForm, CartUpdateQuantityProductForm
from .models import CartItems


class CartItemsListView(ListView):
    model = CartItems
    context_object_name = 'cart_items'
    template_name = 'cart.html'
    extra_context = {'title': _("Cart")}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object_list:
            if len(self.object_list) > 1:
                context['total_cost'] = 0
                context['old_total_cost'] = 0
                for item in self.object_list:
                    item.old_price = get_object_or_404(ShopProduct, product=item.product, shop__slug=item.shop).price
                    if item.product.discount:
                        if item.product.discount.discount_type.id == 2:
                            item.price = _check_doublet_discount(self.object_list, item)
                        if item.product.discount.discount_type.id == 3:
                            item.price = _check_cart_discount(item)

                    context['total_cost'] += (item.quantity * item.price)
                    context['old_total_cost'] += (item.quantity * item.old_price)
                    item.shops_form = CartShopsForm(product=item.product, item_id=item.id)
                    item.update_quantity_form = CartUpdateQuantityProductForm(initial={'quantity': item.quantity,
                                                                                       'item_id': item.id})
            else:
                item = self.object_list[0]
                item.old_price = get_object_or_404(ShopProduct, product=item.product, shop__slug=item.shop).price

                if item.product.discount:
                    if item.product.discount.discount_type.id == 2:
                        item.price = _check_doublet_discount(self.object_list, item)
                    if item.product.discount.discount_type.id == 3:
                        item.price = _check_cart_discount(item)

                context['total_cost'] = item.price * item.quantity
                context['old_total_cost'] = item.quantity * item.old_price
                shops = CartItems().get_shops_for_cart_item(product=item.product)
                shop_list = [shop.shop.name for shop in shops]
                item.shops = shop_list
                item.shops_form = CartShopsForm(product=item.product, item_id=item.id)
                item.update_quantity_form = CartUpdateQuantityProductForm(initial={'quantity': item.quantity,
                                                                                   'item_id': item.id})

        return context

    def get_queryset(self):
        return CartItems().get_cart_items(request=self.request).order_by('-added_at')


def _check_cart_discount(discount_cart_product):
    if discount_cart_product.quantity >= discount_cart_product.product.discount.discount_amount:
        discount = discount_cart_product.old_price * decimal.Decimal(
            (discount_cart_product.product.discount.discount_value / 100))
        new_price = round(discount_cart_product.old_price - discount, 2)
        if discount_cart_product.price > new_price:
            discount_cart_product.price = new_price
            discount_cart_product.save()
    else:
        shop_product = discount_cart_product.get_shops_for_cart_item(discount_cart_product.product.id)[0]
        discount_value = shop_product.get_discount()
        discount = discount_cart_product.old_price * decimal.Decimal((discount_value / 100))
        new_price = round(discount_cart_product.old_price - discount, 2)
        discount_cart_product.price = new_price
        discount_cart_product.save()
    return discount_cart_product.price


def _check_doublet_discount(cart_products, discount_cart_product):
    accept_discount_products = []
    for product in cart_products:
        if discount_cart_product.product.discount == product.product.discount:
            accept_discount_products.append(product)
    if len(accept_discount_products) >= 2 and discount_cart_product.product.discount_doublet:
        discount = discount_cart_product.old_price * decimal.Decimal(
            (discount_cart_product.product.discount.discount_value / 100))
        new_price = round(discount_cart_product.old_price - discount, 2)
        if discount_cart_product.price > new_price:
            discount_cart_product.price = new_price
            discount_cart_product.save()
    else:
        shop_product = discount_cart_product.get_shops_for_cart_item(discount_cart_product.product.id)[0]
        discount_value = shop_product.get_discount()
        discount = discount_cart_product.old_price * decimal.Decimal((discount_value / 100))
        new_price = round(discount_cart_product.old_price - discount, 2)
        discount_cart_product.price = new_price
        discount_cart_product.save()
    return discount_cart_product.price


@require_POST
def cart_add(request, slug):
    """ Представление для добавления товара в корзину из детальной страницы товара без выбора продавца """
    cart = CartItems()
    product = get_object_or_404(Product, slug=slug)
    shop = None
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(request=request,
                 product=product,
                 shop=shop,
                 quantity=cd['quantity']
                 )
        messages.success(request, f'{product.name}' + _(' successfully added to cart!'))
    return redirect('product_detail', slug=slug)


@require_POST
def cart_shop_add(request, slug1, slug2):
    """ Представление для добавления товара в корзину с выбранным продавцом """
    cart = CartItems()
    product = get_object_or_404(Product, slug=slug1)
    cart.add(request=request,
             product=product,
             shop=slug2,
             )
    messages.success(request, f'{product.name}' + _(' successfully added to cart!'))
    return redirect('shops')


def cart_random_shop_add(request, slug):
    """ Представление для добавления товара в корзину с случайным продавцом """
    cart = CartItems()
    product = get_object_or_404(Product, slug=slug)
    cart.add(request, product)
    messages.success(request, f'{product.name}' + _(' successfully added to cart!'))
    return redirect('shops')


def cart_remove(request, **kwargs):
    """ Представление для удаления товара из корзины """
    item_id = kwargs['pk']
    cart = CartItems()
    cart.remove_cart_item(item_id)
    return redirect('cart_detail')


@require_POST
def cart_update_quantity(request, **kwargs):
    """ Представление для обновления количества товара в корзине """
    item_id = kwargs['pk']
    cart = CartItems()
    cart.update_cart_quantity(request, item_id)
    return redirect('cart_detail')


@require_POST
def cart_update_price(request, **kwargs):
    """ Представление для обновления магазина и цены товара в корзине """
    item_id = kwargs['pk']
    cart = CartItems()
    cart.update_cart_price(request, item_id)
    return redirect('cart_detail')
