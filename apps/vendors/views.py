from rest_framework.views import APIView, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from apps.vendors.permissions import IsVendorOwner

from .models import Vendor
from .serializers import VendorSerializer, LocationSerializer, LogoUploadSerializer, BannerUploadSerializer, VendorStatusSerializer



class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "location", "upload_logo", "upload_banner", "status"]:
            return [IsAuthenticated(), IsVendorOwner()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=["patch"])
    def location(self, request, pk=None):
        vendor = self.get_object()

        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            vendor.latitude = serializer.validated_data['latitude']
            vendor.longitude = serializer.validated_data['longitude']
            vendor.save()

            return Response({
                "message": "Location updated",
                "latitude": vendor.latitude,
                "longitude": vendor.longitude
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=["post"])
    def upload_logo(self, request, pk=None):
        vendor = self.get_object()

        serializer = LogoUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vendor.logo = serializer.validated_data["logo"]
        vendor.save()

        return Response({
            "message": "Logo uploaded",
            "logo_url": vendor.logo.url
        })
    
    @action(detail=True, methods=["post"])
    def upload_banner(self, request, pk=None):
        vendor = self.get_object()

        serializer = BannerUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vendor.banner = serializer.validated_data["banner"]
        vendor.save()

        return Response({
            "message": "Banner uploaded",
            "banner_url": vendor.banner.url
        })
    
    @action(detail=True, methods=["patch"])
    def status(self, request, pk=None):
        vendor = self.get_object()

        serializer = VendorStatusSerializer(data=request.data)
        if serializer.is_valid():
            vendor.is_active = serializer.validated_data['is_active']
            vendor.save()

            return Response({
                "message": "Vendor status updated",
                "is_active": vendor.is_active
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)