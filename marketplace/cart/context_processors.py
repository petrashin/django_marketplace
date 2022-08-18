from marketplace import settings
from .models import CartItems


def cart_items_processor(request):
    cart_items = {
        'cart_items': CartItems.objects.filter(session_id=request.session.get(settings.CART_SESSION_ID))

    }
    return cart_items
