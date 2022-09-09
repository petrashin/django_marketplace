from django.urls import path

from app_users.views import *

urlpatterns = [
    path('profile/', ProfileTemplateView.as_view(), name='profile')
]
