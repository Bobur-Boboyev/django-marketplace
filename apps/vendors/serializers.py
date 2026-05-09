from rest_framework import serializers
from django.utils.text import slugify

from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"
        read_only_fields = ("id", "slug", "is_active", "created_at", "updated_at", "status", "user", "is_verified", "is_featured", "rating")

    def create(self, validated_data):
        base_slug = slugify(validated_data['name'])
        slug = base_slug
        counter = 1

        while Vendor.objects.filter(slug=slug).exists():
            validated_data['slug'] = f"{slugify(validated_data['name'])}-{counter}"
            slug = validated_data['slug'] + "-" + str(counter)
            counter += 1

        validated_data['slug'] = slugify(validated_data['name'])

        return super().create(validated_data)
    

class LocationSerializer(serializers.Serializer):
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
    

class LogoUploadSerializer(serializers.Serializer):
    logo = serializers.ImageField()

    def validate_logo(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Logo must be less than 5MB")
        return value
    
class BannerUploadSerializer(serializers.Serializer):
    banner = serializers.ImageField()

    def validate_banner(self, value):
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Banner must be less than 10MB")
        return value


class VendorStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()