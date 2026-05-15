from rest_framework import serializers
from apps.wishlist.models import Wishlist
from apps.products.serializer import ProductSerializer


class WishlistSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "product", "product_detail", "created_at"]
