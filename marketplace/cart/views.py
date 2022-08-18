from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from app_goods.models import Product
from .forms import CartAddProductForm, CartShopsForm, CartUpdateQuantityProductForm
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
                for item in self.object_list:
                    item_cost = item.quantity * item.price
                    context['total_cost'] += item_cost
                    shops = CartItems().get_shops_for_cart_item(product=item.product)
                    shop_list = [shop.shop.name for shop in shops]
                    item.shops = shop_list
                    item.shops_form = CartShopsForm()
                    item.update_quantity_form = CartUpdateQuantityProductForm(initial={'quantity': item.quantity,
                                                                                       'item_id': item.id})
            else:
                item = self.object_list[0]
                context['total_cost'] = item.price * item.quantity
                shops = CartItems().get_shops_for_cart_item(product=item.product)
                shop_list = [shop.shop.name for shop in shops]
                item.shops = shop_list
                item.update_quantity_form = CartUpdateQuantityProductForm(initial={'quantity': item.quantity,
                                                                                   'item_id': item.id})

        return context


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
