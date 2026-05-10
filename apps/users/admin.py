from django.contrib import admin
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

    search_fields = ("email", "first_name", "last_name")

    list_filter = ("is_active", "is_staff")

    ordering = ("-id",)

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "email",
                "first_name",
                "last_name",
                "phone",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
            )
        }),

        ("Role & Identity", {
            "fields": (
                "role_display",
                "is_vendor",
            )
        }),

        ("System Info", {
            "fields": (
                "date_joined",
                "updated_at",
            )
        }),
    )

    readonly_fields = (
        "date_joined",
        "updated_at",
        "role_display",
        "is_vendor",
    )

    def role_display(self, obj):
        return "Vendor" if obj.is_vendor else "Customer"

    role_display.short_description = "Role"

    def is_vendor(self, obj):
        return obj.vendors.filter(status="active").exists()

    is_vendor.boolean = True
    is_vendor.short_description = "Active Vendor"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("vendors")