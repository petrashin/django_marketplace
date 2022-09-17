from django.urls import path
from .views import OrderView, OrderPayment, OrderRepeat

urlpatterns = [
    path('cart/order', OrderView.as_view(), name='order'),
    # path('order/delivery', OrderDelivery.as_view(), name='order_delivery'),
    path('cart/payment', OrderPayment.as_view(), name='order_payment'),
    # path('order/total', OrderTotal.as_view(), name='order_total'),
    # path('order/card', OrderCard.as_view(), name='profile_card'),
    path('repeat', OrderRepeat.as_view(), name='order_repeat'),
]
