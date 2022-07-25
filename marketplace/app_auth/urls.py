from django.urls import path
from app_auth.views import Login, register_view, Logout

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', Logout.as_view(), name='logout'),
]
