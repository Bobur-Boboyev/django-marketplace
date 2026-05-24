from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from .models import Product
from .serializer import ProductSerializer, ProductImageUploadSerializer
from .permissions import IsVendorOwner
from .filters import filter_products
from apps.reviews.serializers import ReviewSerializer
from .recomendations import similar_products



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return []

        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "my_products",
            "upload_image",
            "delete_image",
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

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @extend_schema(request=ProductImageUploadSerializer)
    @action(detail=True, methods=["post"])
    def upload_image(self, request, slug=None):
        product = self.get_object()

        serializer = ProductImageUploadSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        image = ProductImage.objects.create(
            product=product, image=serializer.validated_data["image"]
        )

        return Response(
            {
                "message": "Image uploaded",
                "image_id": image.id,
                "image_url": image.image.url,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["delete"])
    def delete_image(self, request, slug=None):
        product = self.get_object()

        image_id = request.data.get("image_id")

        if not image_id:
            return Response(
                {"detail": "image_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        image = product.images.filter(id=image_id).first()

        if not image:
            return Response(
                {"detail": "Image not found"}, status=status.HTTP_404_NOT_FOUND
            )

        image.image.delete(save=False)
        image.delete()

        return Response({"message": "Image deleted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def reviews(self, request, slug=None):
        product = self.get_object()

        reviews = product.reviews.all()

        serializer = ReviewSerializer(reviews, many=True, context={"request": request})

        return Response(
            {
                "success": True,
                "product": product.name,
                "average_rating": product.average_rating,
                "count": product.reviews_count,
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    
    @action(detail=False, methods=["get"], url_path="similar")
    def similar(self, request):
        product_id = request.query_params.get("product_id")

        if not product_id:
            return Response(
                {"detail": "product_id query param is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = similar_products(product_id)

        serializer = ProductSerializer(results, many=True, context={"request": request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        queryset = Product.objects.filter(
            status=Product.Status.PENDING, is_deleted=False
        )

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
