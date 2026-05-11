from rest_framework.views import APIView, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializer import ProductSerializer
from apps.vendors.permissions import IsVendorOwner
from .filters import filter_products


class ProductListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsVendorOwner()]
        
        return []

    def get(self, request):
        queryset = Product.objects.all()

        products = filter_products(queryset, request.query_params)
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)