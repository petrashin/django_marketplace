from django.contrib import admin
from .models import Billing, PayStatus


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    readonly_fields = ["order", "time_stamp", "card_num", "payment_amount", "payment_status"]


@admin.register(PayStatus)
class PayStatusAdmin(admin.ModelAdmin):
    fields = ['title']
