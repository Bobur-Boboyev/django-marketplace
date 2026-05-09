from django.contrib import admin

from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "vendor_type", "status")
    list_filter = ("vendor_type", "status")
    search_fields = ("name", "email")