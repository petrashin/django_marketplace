from django.contrib import admin

from .models import Delivery, PayMethod, Order


# @admin.register(Delivery)
# class DeliveryAdmin(admin.ModelAdmin):
# 	list_display = ['title']
#
#
# @admin.register(PayMethod)
# class PayMethodAdmin(admin.ModelAdmin):
# 	list_display = ['title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	readonly_fields = ["payment_error"]
	
	def has_delete_permission(self, *args, **kwargs):
		return False


	#
	# def __init__(self, *args, **kwargs):
	# 	super(OrderAdmin, self).__init__(*args, **kwargs)
	# 	self.list_display_links = (None,)
	#
	# # to hide change and add buttons on main page:
	# def get_model_perms(self, request):
	# 	return {'view': True}
