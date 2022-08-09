from django.urls import path
from app_account.views import account_view

urlpatterns = [
    path('', account_view, name='account')
]
