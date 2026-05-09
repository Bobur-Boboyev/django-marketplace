from rest_framework.views import APIView, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.vendors.permissions import IsVendorOwner

from .models import Vendor
from .serializers import VendorSerializer

class VendorListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendors = Vendor.objects.filter(user=request.user)
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VendorSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            serializer.save(user=user)
            user.role = 'vendor'
            user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class VendorDetailAPIView(APIView):
    
    def get_permissions(self):

        if self.request.method == "GET":
            return []

        return [
            IsAuthenticated(),
            IsVendorOwner()
        ]

    def get_object(self, pk):
        vendor = get_object_or_404(Vendor, pk=pk)

        self.check_object_permissions(
            self.request,
            vendor
        )

        return vendor
    
    def get(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    
    def put(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(
            vendor,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def patch(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(
            vendor,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        vendor = self.get_object(pk)

        vendor.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)