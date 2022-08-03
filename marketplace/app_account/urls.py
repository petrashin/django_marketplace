from django.urls import path
from app_account.views import BaseTemplateView

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='account')
]
