from django.urls import path

from app_users.views import BaseTemplateView

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='home')
]
