from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, AdminProductViewSet


router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"admin/products", AdminProductViewSet, basename="admin-products")

urlpatterns = router.urls
