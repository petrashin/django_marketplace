from django.urls import path
from app_account.views import account_view, EditProfile

urlpatterns = [
    path('', account_view, name='account'),
    path('profile/', EditProfile.as_view(), name='profile'),
]
