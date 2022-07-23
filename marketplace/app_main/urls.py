from django.urls import path
from .views import *

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='home'),
]