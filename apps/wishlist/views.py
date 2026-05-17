from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.wishlist.models import Wishlist
from apps.wishlist.serializers import WishlistSerializer
from apps.products.models import Product


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Wishlist.objects.filter(user=request.user).select_related("product")

        serializer = WishlistSerializer(queryset, many=True)

        return Response(serializer.data)

    @extend_schema(
        request=WishlistSerializer,
        responses={200: None},
    )
    def post(self, request):
        product_id = request.data.get("product")

        product = get_object_or_404(Product, id=product_id)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user, product_id=product_id
        )

        if not created:
            return Response(
                {"detail": "Product already in wishlist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = WishlistSerializer(wishlist_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        product_id = request.data.get("product")

        deleted_count, _ = Wishlist.objects.filter(
            user=request.user, product_id=product_id
        ).delete()

        if deleted_count == 0:
            return Response(
                {"detail": "Wishlist item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"detail": "Removed from wishlist"}, status=status.HTTP_204_NO_CONTENT
        )
