from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    autocomplete_fields = ("product",)

    readonly_fields = (
        "price",
        "created_at",
    )

    fields = (
        "product",
        "price",
        "quantity",
        "status",
        "created_at",
    )

    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_price",
        "status_badge",
        "is_paid",
        "created_at",
    )

    list_filter = (
        "is_paid",
        "created_at",
        "items__status",
    )

    search_fields = (
        "id",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "total_price",
        "created_at",
        "status_badge",
    )

    inlines = [OrderItemInline]

    ordering = ("-created_at",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user").prefetch_related("items")

    def status_badge(self, obj):
        return obj.status

    status_badge.short_description = "Status"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order__id",
        "product__name",
        "order__user__username",
    )

    autocomplete_fields = (
        "order",
        "product",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = ("-created_at",)

    actions = (
        "mark_confirmed",
        "mark_shipped",
        "mark_delivered",
        "mark_cancelled",
    )

    @admin.action(description="Mark selected items as CONFIRMED")
    def mark_confirmed(self, request, queryset):
        queryset.update(status=OrderItem.Status.CONFIRMED)

    @admin.action(description="Mark selected items as SHIPPED")
    def mark_shipped(self, request, queryset):
        queryset.update(status=OrderItem.Status.SHIPPED)

    @admin.action(description="Mark selected items as DELIVERED")
    def mark_delivered(self, request, queryset):
        queryset.update(status=OrderItem.Status.DELIVERED)

    @admin.action(description="Mark selected items as CANCELLED")
    def mark_cancelled(self, request, queryset):
        queryset.update(status=OrderItem.Status.CANCELLED)