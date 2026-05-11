from rest_framework.views import APIView, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action

from apps.vendors.permissions import IsVendorOwner

from .models import Vendor
from .serializers import (
    VendorSerializer,
    LocationSerializer,
    LogoUploadSerializer,
    BannerUploadSerializer,
)


class VendorViewSet(ModelViewSet):
    serializer_class = VendorSerializer
    # lookup_field = "slug"

    def get_queryset(self):

        user = self.request.user

        if user.is_staff:
            return Vendor.objects.all()

        return Vendor.objects.filter(status=Vendor.Status.ACTIVE)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in [
            "update",
            "partial_update",
            "destroy",
            "location",
            "upload_logo",
            "upload_banner",
            "delete_logo",
            "delete_banner",
            "status",
            "activate",
            "deactivate",
        ]:
            return [IsAuthenticated(), IsVendorOwner()]

        if self.action in ["approve", "reject", "pending"]:
            return [IsAuthenticated(), IsAdminUser()]

        if self.action == "post":
            return [IsAuthenticated()]

        return []

    @action(detail=True, methods=["patch"])
    def location(self, request, pk=None):
        vendor = self.get_object()

        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            vendor.latitude = serializer.validated_data["latitude"]
            vendor.longitude = serializer.validated_data["longitude"]
            vendor.save()

            return Response(
                {
                    "message": "Location updated",
                    "latitude": vendor.latitude,
                    "longitude": vendor.longitude,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def upload_logo(self, request, pk=None):
        vendor = self.get_object()

        serializer = LogoUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vendor.logo = serializer.validated_data["logo"]
        vendor.save()

        return Response({"message": "Logo uploaded", "logo_url": vendor.logo.url})

    @action(detail=True, methods=["delete"])
    def delete_logo(self, request, pk=None):
        vendor = self.get_object()

        if vendor.logo:
            vendor.logo.delete(save=False)

        vendor.logo = None
        vendor.save()

        return Response({"message": "Logo deleted"})

    @action(detail=True, methods=["post"])
    def upload_banner(self, request, pk=None):
        vendor = self.get_object()

        serializer = BannerUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vendor.banner = serializer.validated_data["banner"]
        vendor.save()

        return Response({"message": "Banner uploaded", "banner_url": vendor.banner.url})

    @action(detail=True, methods=["delete"])
    def delete_banner(self, request, pk=None):
        vendor = self.get_object()

        if vendor.banner:
            vendor.banner.delete(save=False)

        vendor.banner = None
        vendor.save()

        return Response({"message": "Banner deleted"})

    @action(detail=True, methods=["patch"])
    def activate(self, request, pk=None):
        vendor = self.get_object()

        vendor.activate()

        return Response({"message": "Vendor activated", "is_active": vendor.is_active})

    @action(detail=True, methods=["patch"])
    def deactivate(self, request, pk=None):
        vendor = self.get_object()

        vendor.deactivate()

        return Response(
            {"message": "Vendor deactivated", "is_active": vendor.is_active}
        )


class AdminVendorViewSet(ReadOnlyModelViewSet):
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Vendor.objects.all()

    @action(detail=True, methods=["patch"])
    def approve(self, request, pk=None):
        vendor = self.get_object()

        vendor.approve()

        return Response(
            {
                "message": "Vendor approved",
                "status": vendor.status,
            }
        )

    @action(detail=True, methods=["patch"])
    def reject(self, request, pk=None):
        vendor = self.get_object()

        reason = request.data.get("reason", "Vendor application rejected.")

        vendor.reject(reason)

        return Response(
            {
                "message": "Vendor rejected",
                "status": vendor.status,
                "reason": vendor.rejection_reason,
            }
        )

    @action(detail=False, methods=["get"])
    def pending(self, request):

        pending_vendors = Vendor.objects.filter(status=Vendor.Status.PENDING)

        serializer = self.get_serializer(pending_vendors, many=True)

        return Response(serializer.data)
