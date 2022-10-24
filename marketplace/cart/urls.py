from django.urls import path
from .views import *


urlpatterns = [
    path('', CartItemsListView.as_view(), name='cart_detail'),
    path('add/<slug:slug>/', cart_add, name='cart_add'),
    path('remove/<int:pk>/', cart_remove, name='cart_remove'),
    path('update/<int:pk>/', cart_update_quantity, name='cart_update_quantity'),
    path('update_price/<int:pk>/', cart_update_price, name='cart_update_price'),
    path('add_shop/<slug:slug1>/<slug:slug2>', cart_shop_add, name='cart_shop_add'),
    path('add_random_shop/<slug:slug>/', cart_random_shop_add, name='cart_random_shop_add'),
]
