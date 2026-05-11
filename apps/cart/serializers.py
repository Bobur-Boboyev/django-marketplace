from rest_framework import serializers
from .models import Cart, CartItem
from apps.products.models import Product
from apps.products.serializer import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total"]

    def get_total(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "items"]


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(default=1, min_value=1)

    def validate(self, data):

        try:
            product = Product.objects.get(id=data["product_id"], is_deleted=False)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Product not found"})

        data["product"] = product
        return data


class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)

    def validate(self, data):

        try:
            product = Product.objects.get(id=data["product_id"], is_deleted=False)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Product not found"})

        data["product"] = product
        return data


class UpdateCartQuantitySerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=0)

    def validate(self, data):

        try:
            product = Product.objects.get(id=data["product_id"], is_deleted=False)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Product not found"})

        data["product"] = product
        return data
