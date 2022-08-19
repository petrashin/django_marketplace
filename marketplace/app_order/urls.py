from django.urls import path
from .views import OrderUserView, OrderDeliveryView, OrderPayMethodView, OrderTotal

urlpatterns = [
    path('cart/order', OrderUserView.as_view(), name='order'),
	path('cart/order/delivery', OrderDeliveryView.as_view(),name='delivery'),
	path('cart/order/pay_method', OrderPayMethodView.as_view(),name='pay_method'),
	path('cart/order/total', OrderTotal.as_view(),name='pay_method'),
]
