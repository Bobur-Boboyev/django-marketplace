from django.contrib import admin
from django.utils.html import format_html

from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):

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
            "fields": (
                "user",
            )
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
            "fields": (
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
        if obj:
            return (
                "user",
                "rating",
                "review_count",
                "created_at",
                "updated_at",
                "logo_preview",
                "logo_preview_small",
                "banner_preview",
            )
        
        return (
            "slug",
            "is_active",
            "is_featured",
            "is_deleted",
            "rating",
            "review_count",
            "created_at",
            "updated_at",
            "last_active_at",
            "logo_preview",
            "logo_preview_small",
            "banner_preview",

        )

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

    logo_preview.short_description = "Logo Preview"

    def banner_preview(self, obj):
        if obj.banner:
            return format_html(
                '<img src="{}" style="width:300px;height:120px;border-radius:10px;object-fit:cover;" />',
                obj.banner.url
            )
        return "No banner"

    banner_preview.short_description = "Banner Preview"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")