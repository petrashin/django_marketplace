from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Shop, ShopProduct, ShopImage


class ShopImageInline(admin.TabularInline):
    model = ShopImage
    raw_id_fields = ['shop']
    extra = 0


class ShopProductInline(admin.TabularInline):
    model = ShopProduct
    row_id_fields = ['shop']
    extra = 0


@admin.register(Shop)
class ShopAdmin(TranslationAdmin):
    list_display = ['name', 'about', 'country', 'city', 'street']
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ShopProductInline, ShopImageInline)
