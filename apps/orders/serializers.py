from rest_framework import serializers
from django.db import transaction

from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem
from apps.cart.utils import get_cart


class CreateOrderSerializer(serializers.Serializer):
    pass

    def create(self, validated_data, user):
        cart = get_cart(user)
        items = cart.items.select_related("product")

        if not items.exists():
            raise serializers.ValidationError("Cart is empty")

        with transaction.atomic():
            order = Order.objects.create(user=user)

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
