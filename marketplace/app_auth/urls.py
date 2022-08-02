from django.contrib.auth import views as auth_views
from django.urls import path

from app_auth.views import Login, Logout, password_reset_request, register_view

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
]
