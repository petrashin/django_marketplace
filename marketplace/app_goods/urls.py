from django.urls import path

from app_goods.views import *

urlpatterns = [
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('review/<slug:slug>/', AddReview.as_view(), name='add_review'),
    path('discounts/', DiscountListView.as_view(), name='discounts')
]