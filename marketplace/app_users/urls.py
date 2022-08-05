from django.urls import path

from app_users.views import AddReview

urlpatterns = [
    path('add_review/', AddReview.as_view(), name='add_review')
]
