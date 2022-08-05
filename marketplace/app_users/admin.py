from django.contrib import admin
from .models import Profile, Reviews, Role


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Reviews)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Role)
class ProfileAdmin(admin.ModelAdmin):
    pass

