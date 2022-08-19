from django.contrib import admin
from .models import Shop, ShopProduct


class ShopProductInline(admin.TabularInline):
    model = ShopProduct
    row_id_fields = ['shop']
    extra = 0


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ShopProductInline, )
