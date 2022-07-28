from app_main.models import Profile, Role
from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Role)
class ProfileAdmin(admin.ModelAdmin):
    pass