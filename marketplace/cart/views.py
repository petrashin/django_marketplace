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
                    context['total_cost'] += (item.quantity * item.price)
                    context['old_total_cost'] += (item.quantity * item.old_price)
                    item.shops_form = CartShopsForm(product=item.product, item_id=item.id)
                    item.update_quantity_form = CartUpdateQuantityProductForm(initial={'quantity': item.quantity,
                                                                                       'item_id': item.id})
            else:
                item = self.object_list[0]
                item.old_price = get_object_or_404(ShopProduct, product=item.product, shop__name=item.shop).price
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


@require_POST
def cart_add(request, slug):
    cart = CartItems()
    product = get_object_or_404(Product, slug=slug)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(request=request,
                 product=product,
                 quantity=cd['quantity']
                 )
    return redirect('cart_detail')


@require_POST
def cart_shop_add(request, slug):
    cart = CartItems()
    product = get_object_or_404(Product, slug=slug)
    form = CartAddProductShopForm(request.POST)
    print('form:', form)
    if form.is_valid():
        cd = form.cleaned_data
        print('cd: ', cd)
        cart.add(request=request,
                 product=product,
                 quantity=cd['quantity']
                 )
    return redirect('cart_detail')


def cart_remove(request, **kwargs):
    item_id = kwargs['pk']
    cart = CartItems()
    cart.remove_cart_item(request, item_id)
    return redirect('cart_detail')


def cart_update_quantity(request, **kwargs):
    item_id = kwargs['pk']
    cart = CartItems()
    cart.update_cart_quantity(request, item_id)
    return redirect('cart_detail')


def cart_update_price(request, **kwargs):
    item_id = kwargs['pk']
    cart = CartItems()
    cart.update_cart_price(request, item_id)
    return redirect('cart_detail')
