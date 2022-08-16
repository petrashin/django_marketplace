from .models import CartItems


def cart_items_processor(request):
    cart_items = {
        'cart_items': CartItems.objects.filter(user=request.user.id, session_id=request.session.session_key)


    }
    return cart_items
