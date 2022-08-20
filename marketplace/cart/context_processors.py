from .models import CartItems


def cart(request):
    return {'cart': CartItems().get_cart_items(request)}