from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("created_at",)
    autocomplete_fields = ("product",)
    show_change_link = True


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_items", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    inlines = [CartItemInline]
    readonly_fields = ("created_at", "updated_at")

    def total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
    total_items.short_description = "Total Items"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity", "created_at")
    list_filter = ("created_at",)
    search_fields = ("cart__user__username", "product__name")
    autocomplete_fields = ("cart", "product")
    readonly_fields = ("created_at",)