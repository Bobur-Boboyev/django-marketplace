from rest_framework import serializers
from django.utils.text import slugify

from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"
        read_only_fields = ("id", "slug", "is_active", "created_at", "updated_at", "status", "user", "is_verified", "is_featured")

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
    
