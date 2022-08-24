from .models import CartItems


def cart(request):
    return {'cart': CartItems().get_cart_items(request),
            'cart_total_cost': CartItems().get_total_cost(request)
            }