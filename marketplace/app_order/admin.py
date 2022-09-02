from django.contrib import admin
from .models import Delivery, PayMethod, Order


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
	list_display = ['title']


@admin.register(PayMethod)
class PayMethodAdmin(admin.ModelAdmin):
	list_display = ['title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	readonly_fields = ["payment_status"]
	
	def has_delete_permission(self, *args, **kwargs):
		return False
