from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    raw_id_fields = ['product']
    extra = 0


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['name', 'slug', 'published']
    prepopulated_fields = {'slug': ('name',)}

    def has_delete_permission(self, *args, **kwargs):
        return False


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['name', 'slug', 'published']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    def has_delete_permission(self, *args, **kwargs):
        return False


@admin.register(Discount)
class DiscountAdmin(TranslationAdmin):
    pass


@admin.register(Reviews)
class ReviewsAdmin(TranslationAdmin):
    list_display = ['product', 'text', 'user', 'published']
