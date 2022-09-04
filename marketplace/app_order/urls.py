from django.urls import path
from .views import OrderView, OrderPayment

urlpatterns = [
    path('cart/order', OrderView.as_view(), name='order'),
    path('cart/payment', OrderPayment.as_view(), name='payment'),
]
