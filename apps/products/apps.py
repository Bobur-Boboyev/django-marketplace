from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"


    def ready(self):
        from .qdrant import init_qdrant

        try:
            init_qdrant()
        except Exception as e:
            print(f"Error initializing Qdrant: {e}")