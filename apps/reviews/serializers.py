from rest_framework import serializers
from apps.reviews.models import Review
from apps.orders.models import OrderItem


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "product", "rating", "comment", "created_at"]
        read_only_fields = ["user"]

    def validate_rating(self, value):
        if value < 1 and value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        product = attrs.get("product")
        has_purchased = OrderItem.objects.filter(
            order__user=user, order__is_paid=True, product=product
        ).exists()
        if not has_purchased:
            raise serializers.ValidationError("You can only review purchased products")
        return attrs
