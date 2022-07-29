from django.urls import path

from app_shops.views import *

urlpatterns = [
    path('shop/', ShopTemplateView.as_view(), name='shop_detail'),
]