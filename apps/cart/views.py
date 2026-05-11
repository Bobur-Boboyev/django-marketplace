from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.products.models import Product
from .models import CartItem
from .utils import get_cart


class AddToCartView(APIView):
    def post(self, request):

        cart = get_cart(request.user)

        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        product = Product.objects.filter(id=product_id, is_deleted=False).first()

        if not product:
            return Response(
                {"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response({"message": "Added to cart"}, status=status.HTTP_200_OK)
