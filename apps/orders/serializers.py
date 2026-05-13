from rest_framework import serializers
from django.db import transaction

from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem
from apps.payments.models import Invoice
from apps.cart.utils import get_cart


class CreateOrderSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        cart = get_cart(user)
        items = cart.items.select_related("product")

        if not items.exists():
            raise serializers.ValidationError("Cart is empty")

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                latitude=validated_data["latitude"],
                longitude=validated_data["longitude"],
            )

            total = 0

            for item in items:
                product = item.product

                if product.stock < item.quantity:
                    raise serializers.ValidationError(
                        f"Not enough stock for {product.name}"
                    )

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=item.quantity,
                )

                product.stock -= item.quantity
                product.save()

                total += product.price * item.quantity

            order.total_price = total
            order.save()

            cart.items.all().delete()

        return order


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_name",
            "price",
            "quantity",
            "status",
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ["id", "status", "total_price", "created_at", "items"]


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ["id", "status", "total_price", "created_at"]


class UpdateOrderItemStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderItem.Status.choices)
