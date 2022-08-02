from django.urls import path

from app_main.views import BaseTemplateView, AddReview

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='home'),
    path('add_review/', AddReview.as_view(), name='add_review')
]
