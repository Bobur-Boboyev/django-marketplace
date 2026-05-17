from rest_framework import serializers
from django.utils.text import slugify

from .models import Product, ProductImage, Category


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = [
            "status",
            "rejection_reason",
            "slug",
            "average_rating",
            "reviews_count",
        ]

    def create(self, validated_data):
        base_slug = slugify(validated_data["name"])
        slug = base_slug
        counter = 1

        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        validated_data["slug"] = slug
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "name" in validated_data and instance.name != validated_data["name"]:
            base_slug = slugify(validated_data["name"])
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exclude(id=instance.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            validated_data["slug"] = slug

        return super().update(instance, validated_data)


class ProductImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
