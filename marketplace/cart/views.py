import decimal

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from app_goods.models import Product
from app_shops.models import ShopProduct
from .forms import CartAddProductForm, CartAddProductShopForm, CartShopsForm, CartUpdateQuantityProductForm
from .models import CartItems


class CartItemsListView(ListView):
    model = CartItems
    context_object_name = 'cart_items'
    template_name = 'cart.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object_list:
            if len(self.object_list) > 1:
                context['total_cost'] = 0
                context['old_total_cost'] = 0
                for item in self.object_list:
                    item.old_price = get_object_or_404(ShopProduct, product=item.product, shop__name=item.shop).price

                    if item.product.discount.discount_type.id == 3:
                        discount = _check_cart_discount(item, item.old_price)
                        item.price = round(item.price - discount, 2)

                    context['total_cost'] += round(item.price * item.quantity, 2)
                    context['old_total_cost'] += (item.quantity * item.old_price)
                    item.shops_form = CartShopsForm(product=item.product, item_id=item.id)
                    item.update_quantity_form = CartUpdateQuantityProductForm(initial={'quantity': item.quantity,
                                                                                       'item_id': item.id})
            else:
                item = self.object_list[0]
                item.old_price = get_object_or_404(ShopProduct, product=item.product, shop__name=item.shop).price

                if item.product.discount.discount_type.id == 3:
                    discount = _check_cart_discount(item, item.old_price)
                    item.price = round(item.price - discount, 2)

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
        return CartItems().get_cart_items(request=self.request)


def _check_cart_discount(cart_product, old_price):
    discount = 0
    if cart_product.price == old_price:
        if cart_product.quantity >= cart_product.product.discount.discount_amount:
            discount = cart_product.price * decimal.Decimal((cart_product.product.discount.discount_value / 100))
    return discount

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
        messages.success(request, f'{product.name} успешно добавлен в корзину!')
    return redirect('product_detail', slug=slug)


@require_POST
def cart_shop_add(request, slug):
    """ Представление для добавления товара в корзину с выбранным продавцом """
    cart = CartItems()
    product = get_object_or_404(Product, slug=slug)
    form = CartAddProductShopForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(request=request,
                 product=product,
                 shop=cd['shop'],
                 quantity=cd['quantity']
                 )
        messages.success(request, f'{product.name} успешно добавлен в корзину!')
    return redirect('shops')


def cart_remove(request, **kwargs):
    """ Представление для удаления товара из корзины """
    item_id = kwargs['pk']
    cart = CartItems()
    cart.remove_cart_item(item_id)
    return redirect('cart_detail')


def cart_update_quantity(request, **kwargs):
    """ Представление для обновления количества товара в корзине """
    item_id = kwargs['pk']
    cart = CartItems()
    cart.update_cart_quantity(request, item_id)
    return redirect('cart_detail')


def cart_update_price(request, **kwargs):
    """ Представление для обновления магазина и цены товара в корзине """
    item_id = kwargs['pk']
    cart = CartItems()
    cart.update_cart_price(request, item_id)
    return redirect('cart_detail')
