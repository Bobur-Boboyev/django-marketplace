from rest_framework.routers import DefaultRouter

from .views import VendorViewSet, AdminVendorViewSet

router = DefaultRouter()

router.register(
    r"vendors",
    VendorViewSet,
    basename="vendors"
)

router.register(
    r"admin/vendors",
    AdminVendorViewSet,
    basename="admin-vendors"
)

urlpatterns = router.urls