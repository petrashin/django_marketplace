from django.contrib import admin
from .models import Profile, Role


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Role)
class ProfileAdmin(admin.ModelAdmin):
    pass
