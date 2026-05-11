from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import mark_safe

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role_display",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
    )

    ordering = ("-updated_at",)

    readonly_fields = (
        "date_joined",
        "updated_at",
        "role_display",
        "is_vendor",
        "vendors_list",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "Role & Identity",
            {
                "fields": (
                    "role_display",
                    "is_vendor",
                )
            },
        ),
        (
            "System Info",
            {
                "fields": (
                    "date_joined",
                    "updated_at",
                )
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):

        fieldsets = list(super().get_fieldsets(request, obj))

        if obj and obj.is_vendor:
            fieldsets.append(("Vendor Accounts", {"fields": ("vendors_list",)}))

        return fieldsets

    def role_display(self, obj):
        return "Vendor" if obj.is_vendor else "Customer"

    role_display.short_description = "Role"

    def is_vendor(self, obj):
        return obj.vendors.filter(status="active").exists()

    is_vendor.boolean = True
    is_vendor.short_description = "Active Vendor"

    def vendors_list(self, obj):

        vendors = obj.vendors.all()

        html = render_to_string("admin/users/vendor_list.html", {"vendors": vendors})

        return mark_safe(html)

    vendors_list.short_description = "Vendor Accounts"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("vendors")
