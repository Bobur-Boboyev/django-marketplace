from rest_framework.views import APIView, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from apps.vendors.permissions import IsVendorOwner

from .models import Vendor
from .serializers import VendorSerializer



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

        vendor.latitude = request.data.get("latitude", vendor.latitude)
        vendor.longitude = request.data.get("longitude", vendor.longitude)
        vendor.save()

        return Response({
            "message": "Location updated",
            "latitude": vendor.latitude,
            "longitude": vendor.longitude
        })
    
    @action(detail=True, methods=["post"])
    def upload_logo(self, request, pk=None):
        vendor = self.get_object()

        logo = request.FILES.get("logo")
        if not logo:
            return Response({"error": "No logo provided"}, status=status.HTTP_400_BAD_REQUEST)

        vendor.logo = logo
        vendor.save()

        return Response({"message": "Logo uploaded", "logo_url": vendor.logo.url})
    
    @action(detail=True, methods=["post"])
    def upload_banner(self, request, pk=None):
        vendor = self.get_object()

        banner = request.FILES.get("banner")
        if not banner:
            return Response({"error": "No banner provided"}, status=status.HTTP_400_BAD_REQUEST)

        vendor.banner = banner
        vendor.save()

        return Response({"message": "Banner uploaded", "banner_url": vendor.banner.url})
    
    @action(detail=True, methods=["patch"])
    def status(self, request, pk=None):
        vendor = self.get_object()

        vendor.is_active = request.data.get("is_active", vendor.is_active)
        vendor.save()

        return Response({
            "message": "Status updated",
            "is_active": vendor.is_active
        })