from django.urls import path
from .views import OrderView, OrderPayment#, OrderDelivery, OrderTotal, OrderCard

urlpatterns = [
    path('order', OrderView.as_view(), name='order'),
    # path('order/delivery', OrderDelivery.as_view(), name='order_delivery'),
    path('order/payment', OrderPayment.as_view(), name='order_payment'),
    # path('order/total', OrderTotal.as_view(), name='order_total'),
    # path('order/card', OrderCard.as_view(), name='profile_card'),
]
