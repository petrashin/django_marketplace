from django.contrib import admin
from .models import Profile, Role, Image, ViewsHistory, ComparedProducts
from modeltranslation.admin import TranslationAdmin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'phone_number', 'balance', 'role', 'published']
	
	def has_delete_permission(self, *args, **kwargs):
		return False


@admin.register(Role)
class RoleAdmin(TranslationAdmin):
	list_display = ['id', 'name']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
	list_display = ['id', 'profile', 'avatar']


@admin.register(ViewsHistory)
class ViewsHistoryAdmin(admin.ModelAdmin):
	pass


@admin.register(ComparedProducts)
class ComparedProductsAdmin(admin.ModelAdmin):
	pass
