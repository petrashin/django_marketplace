from django.contrib import admin

from app_users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
