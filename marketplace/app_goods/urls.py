from django.urls import path

from app_goods.views import *

urlpatterns = [
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('review/<slug:slug>/', AddReview.as_view(), name='add_review'),
    path('compare/', CompareGoodsView.as_view(), name='compare'),
    path('compare/<int:pk>/delete/', delete_from_comparison, name='delete_from_comparison'),
    path('compare/<int:pk>/add/', add_to_comparison, name='add_to_comparison'),
    path('sale/', SaleView.as_view(), name='sale_list'),
]
