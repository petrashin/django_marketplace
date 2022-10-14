from .models import CartItems


def cart(request):
    return {
            'cart_total_cost': CartItems().get_total_cost(request),
            'cart_total_quantity': CartItems().get_total_quantity(request)
            }
