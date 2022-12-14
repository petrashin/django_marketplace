from django.urls import path

from app_shops.views import *

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='home'),
    path('shops/', ShopListView.as_view(), name='shops'),
    path('shop/<slug:slug>/', ShopDetailView.as_view(), name='shop_detail'),
    path('catalog/', CatalogueView.as_view(), name='search_results'),
    path('catalog/<int:category_id>/', CatalogueView.as_view(), name='catalog'),
]
