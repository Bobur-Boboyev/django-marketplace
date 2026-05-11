from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .models import Product
from .serializer import ProductSerializer
from .permissions import IsVendorOwner
from .filters import filter_products


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = "slug"

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return []

        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "my_products",
        ]:
            return [IsAuthenticated(), IsVendorOwner()]

        return []

    def get_queryset(self):
        queryset = super().get_queryset()
        return filter_products(queryset, self.request.query_params)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.soft_delete()

        return Response({"message": "deleted"}, status=200)

    @action(detail=False, methods=["get"], url_path="my-products")
    def my_products(self, request):
        vendor_id = request.query_params.get("vendor")

        if not vendor_id:
            return Response(
                {"detail": "vendor query param is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            vendor = request.user.vendors.get(id=vendor_id)
        except request.user.vendors.model.DoesNotExist:
            return Response(
                {"detail": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND
            )

        queryset = (
            Product.objects.filter(vendor=vendor)
            .select_related("category", "vendor")
            .prefetch_related("images")
        )

        queryset = filter_products(queryset, request.query_params)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class AdminProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "id"

    queryset = (
        Product.objects.filter(is_deleted=False)
        .select_related("vendor", "category")
        .prefetch_related("images")
    )

    @action(detail=True, methods=["post"])
    def approve(self, request, id=None):
        product = self.get_object()

        product.approve()

        return Response({"detail": "Product approved"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reject(self, request, id=None):

        product = self.get_object()

        rejection_reason = request.data.get("reason")

        if not rejection_reason:
            return Response(
                {"detail": "reason is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        product.reject(reason=rejection_reason)

        return Response({"detail": "Product rejected"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def pending(self, request):
        products = Product.objects.filter(status="pending")
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)
