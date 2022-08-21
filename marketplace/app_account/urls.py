from django.urls import path
from app_account.views import account_view, EditProfile, OrderListView, OrderDetailView

urlpatterns = [
    path('', account_view, name='account'),
    path('profile/', EditProfile.as_view(), name='profile'),
    path('orders/', OrderListView.as_view(), name='orderhistory'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
]
