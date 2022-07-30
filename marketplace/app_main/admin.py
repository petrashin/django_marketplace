from django.contrib import admin
from app_main.models import Profile, Reviews


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Reviews)
class ProfileAdmin(admin.ModelAdmin):
    pass
