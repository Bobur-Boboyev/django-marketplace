from django.contrib import admin
from django.utils.html import format_html

from .models import Vendor
from .forms import VendorAdminForm


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):

    form = VendorAdminForm
    change_form_template = "admin/vendor_change_form.html"

    list_display = (
        "name",
        "email",
        "vendor_type",
        "status",
        "country",
        "city",
        "is_active",
        "is_featured",
        "logo_preview_small",
    )

    list_filter = (
        "vendor_type",
        "status",
        "country",
        "city",
        "is_active",
        "is_featured",
        "is_deleted",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "slug",
    )

    ordering = ("-id",)

    fieldsets = (
        ("Ownership", {
            "fields": ("user",)
        }),

        ("Basic Info", {
            "fields": (
                "name",
                "slug",
                "description",
            )
        }),

        ("Contact", {
            "fields": (
                "email",
                "phone",
                "website",
            )
        }),

        ("Business", {
            "fields": (
                "vendor_type",
                "status",
                "is_active",
                "is_featured",
                "is_deleted",
            )
        }),

        ("Media", {
            "fields": (
                "logo",
                "logo_preview",
                "banner",
                "banner_preview",
            )
        }),

        ("Location", {
            "classes": ("collapse",),
            "fields": (
                "location_button",
                "country",
                "city",
                "address",
                "postal_code",
                "latitude",
                "longitude",
            )
        }),

        ("Legal", {
            "fields": (
                "tax_number",
                "registration_number",
            )
        }),

        ("Stats", {
            "fields": (
                "rating",
                "review_count",
                "last_active_at",
            )
        }),

        ("System", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        base = (
            "rating",
            "review_count",
            "created_at",
            "updated_at",
            "logo_preview",
            "logo_preview_small",
            "banner_preview",
            "location_button",
            "slug",
        )

        if obj:
            return ("user",) + base

        return (
            "is_active",
            "is_featured",
            "is_deleted",
            "last_active_at",
        ) + base

    def location_button(self, obj=None):
        return format_html(
            '<button type="button" id="openMapBtn" style="padding:8px 12px;'
            'background:#0d6efd;color:white;border:none;border-radius:6px;cursor:pointer;">'
            'Location</button>'
        )

    location_button.short_description = "Location Picker"

    def logo_preview_small(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />',
                obj.logo.url
            )
        return "—"

    logo_preview_small.short_description = "Logo"

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="width:120px;height:120px;border-radius:10px;object-fit:cover;" />',
                obj.logo.url
            )
        return "No logo"

    def banner_preview(self, obj):
        if obj.banner:
            return format_html(
                '<img src="{}" style="width:300px;height:120px;border-radius:10px;object-fit:cover;" />',
                obj.banner.url
            )
        return "No banner"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser