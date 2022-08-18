from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    raw_id_fields = ['product']
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


@admin.register(PriceType)
class PriceTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Reviews)
class ProfileAdmin(admin.ModelAdmin):
    pass
