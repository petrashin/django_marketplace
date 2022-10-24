from django.urls import path

from .views import OrderPayment, OrderRepeat, OrderView

urlpatterns = [
    path('cart/order/', OrderView.as_view(), name='order'),
    path('cart/order/<str:pk>', OrderView.as_view(), name='order'),
    path('cart/payment', OrderPayment.as_view(), name='order_payment'),
    path('cart/repeat', OrderRepeat.as_view(), name='order_repeat'),
]
