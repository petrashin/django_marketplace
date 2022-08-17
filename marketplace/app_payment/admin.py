from django.contrib import admin

from .models import Billing


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    pass
