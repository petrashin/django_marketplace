from django.contrib import admin
from .models import Profile, Reviews, Categories

admin.site.register(Categories)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Reviews)
class ProfileAdmin(admin.ModelAdmin):
    pass
