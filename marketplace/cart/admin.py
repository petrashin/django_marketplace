from django.contrib import admin

from .models import CartItems


@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_id', 'product', 'shop', 'price', 'quantity', 'added_at']

