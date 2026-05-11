from rest_framework.permissions import BasePermission
from .models import Product


class IsVendorOwner(BasePermission):
    def has_object_permission(self, request, view, obj: Product):

        return obj.vendor.user == request.user
