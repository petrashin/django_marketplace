from django.contrib import admin

from .models import Billing, PayStatus


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    pass


@admin.register(PayStatus)
class PayStatusAdmin(admin.ModelAdmin):
    fields = ['title']
