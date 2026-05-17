from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.products.models import Product
from .models import CartItem
from .utils import get_cart
from .serializers import (
    CartSerializer,
    AddToCartSerializer,
    RemoveFromCartSerializer,
    UpdateCartQuantitySerializer,
)


@extend_schema(
    request=AddToCartSerializer,
)
class AddToCartView(APIView):
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        product = data["product"]
        quantity = data["quantity"]

        cart = get_cart(request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response({"message": "Added to cart"}, status=status.HTTP_200_OK)


@extend_schema(
    request=RemoveFromCartSerializer,
)
class RemoveFromCartView(APIView):
    def post(self, request):
        serializer = RemoveFromCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        product = data["product"]
        cart = get_cart(request.user)

        item = CartItem.objects.filter(cart=cart, product=product).first()

        if not item:
            return Response(
                {"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        item.delete()

        return Response({"message": "Removed from cart"}, status=status.HTTP_200_OK)


@extend_schema(
    request=UpdateCartQuantitySerializer,
)
class UpdateCartQuantityView(APIView):
    def patch(self, request):
        serializer = UpdateCartQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        product = data["product"]
        quantity = data["quantity"]

        cart = get_cart(request.user)

        item = CartItem.objects.filter(cart=cart, product=product).first()

        if not item:
            return Response(
                {"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if quantity <= 0:
            item.delete()
            return Response({"message": "Item removed"}, status=status.HTTP_200_OK)

        item.quantity = quantity
        item.save()

        return Response({"message": "Quantity updated"}, status=status.HTTP_200_OK)


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_cart(request.user)

        serializer = CartSerializer(cart)

        return Response(serializer.data)
