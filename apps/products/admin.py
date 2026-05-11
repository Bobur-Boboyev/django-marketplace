from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage


class CategoryInline(admin.TabularInline):
    model = Category
    fk_name = "parent"
    extra = 0
    fields = ("name", "slug")
    readonly_fields = ("slug",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent",
        "slug",
    )

    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("parent",)
    ordering = ("name",)

    inlines = [CategoryInline]


class ProductImageInline(admin.TabularInline):
    model = ProductImage

    extra = 1

    readonly_fields = ("image_preview",)

    fields = (
        "image",
        "image_preview",
    )

    def image_preview(self, obj):

        if obj.image:
            return format_html(
                """
                <img 
                    src="{}" 
                    style="
                        width:80px;
                        height:80px;
                        object-fit:cover;
                        border-radius:10px;
                        border:1px solid #eee;
                    "
                />
                """,
                obj.image.url,
            )

        return "No image"

    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

    list_display = (
        "image_preview_small",
        "name",
        "vendor",
        "category",
        "price_display",
        "stock_display",
        "status_badge",
        "is_deleted",
    )

    list_display_links = (
        "image_preview_small",
        "name",
    )

    search_fields = (
        "name",
        "slug",
        "vendor__name",
        "category__name",
    )

    list_filter = (
        "status",
        "is_deleted",
        "category",
        "vendor",
    )

    autocomplete_fields = (
        "vendor",
        "category",
    )

    readonly_fields = ("image_preview_large", "vendor")

    ordering = ("-id",)

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "vendor",
                    "category",
                    "name",
                    "slug",
                    "description",
                )
            },
        ),
        (
            "Pricing & Inventory",
            {
                "fields": (
                    "price",
                    "stock",
                )
            },
        ),
        (
            "Moderation",
            {
                "fields": (
                    "status",
                    "rejection_reason",
                    "is_deleted",
                )
            },
        ),
        ("Preview", {"fields": ("image_preview_large",)}),
    )

    prepopulated_fields = {"slug": ("name",)}

    def image_preview_small(self, obj):

        first_image = obj.images.first()

        if first_image and first_image.image:
            return format_html(
                """
                <img 
                    src="{}"
                    style="
                        width:45px;
                        height:45px;
                        object-fit:cover;
                        border-radius:10px;
                        border:1px solid #eee;
                    "
                />
                """,
                first_image.image.url,
            )

        return format_html(
            """
            <div style="
                width:45px;
                height:45px;
                border-radius:10px;
                background:#f1f3f5;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:11px;
                color:#888;
            ">
                —
            </div>
            """
        )

    image_preview_small.short_description = ""

    def image_preview_large(self, obj):

        images = obj.images.all()

        if not images:
            return "No images"

        html = '<div style="display:flex;gap:10px;flex-wrap:wrap;">'

        for image in images:
            html += f'''
                <img 
                    src="{image.image.url}"
                    style="
                        width:140px;
                        height:140px;
                        object-fit:cover;
                        border-radius:14px;
                        border:1px solid #eee;
                    "
                />
            '''

        html += "</div>"

        return format_html(html)

    image_preview_large.short_description = "Product Gallery"

    def price_display(self, obj):
        return f"${obj.price}"

    price_display.short_description = "Price"

    def stock_display(self, obj):

        color = "#198754"

        if obj.stock <= 0:
            color = "#dc3545"

        elif obj.stock < 5:
            color = "#fd7e14"

        return format_html(
            """
            <span style="
                font-weight:600;
                color:{};
            ">
                {}
            </span>
            """,
            color,
            obj.stock,
        )

    stock_display.short_description = "Stock"

    def status_badge(self, obj):

        colors = {
            "approved": ("#e7f9ee", "#198754"),
            "pending": ("#fff6dd", "#b78103"),
            "rejected": ("#fdecec", "#dc3545"),
            "draft": ("#e9ecef", "#343a40"),
        }

        bg, text = colors.get(obj.status, ("#eee", "#111"))

        return format_html(
            """
            <span style="
                background:{};
                color:{};
                padding:5px 10px;
                border-radius:999px;
                font-size:11px;
                font-weight:600;
                text-transform:uppercase;
            ">
                {}
            </span>
            """,
            bg,
            text,
            obj.status,
        )

    status_badge.short_description = "Status"

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "vendor",
                "category",
            )
            .prefetch_related(
                "images",
            )
        )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "image_preview",
    )

    search_fields = ("product__name",)

    autocomplete_fields = ("product",)

    def image_preview(self, obj):

        if obj.image:
            return format_html(
                """
                <img 
                    src="{}"
                    style="
                        width:80px;
                        height:80px;
                        object-fit:cover;
                        border-radius:10px;
                        border:1px solid #eee;
                    "
                />
                """,
                obj.image.url,
            )

        return "No image"

    image_preview.short_description = "Preview"
