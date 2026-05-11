from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum

from .serializers import (
    CreateOrderSerializer,
    OrderDetailSerializer,
    OrderSerializer,
    UpdateOrderItemStatusSerializer,
)
from .models import Order, OrderItem
from .utils import StandardPagination

from apps.vendors.permissions import IsVendorOwner
from apps.vendors.models import Vendor


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer()

        order = serializer.create(validated_data={}, user=request.user)

        return Response(
            {"message": "Order created", "order_id": order.id},
            status=status.HTTP_201_CREATED,
        )


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")

        paginator = StandardPagination()
        result_page = paginator.paginate_queryset(orders, request)

        serializer = OrderSerializer(result_page, many=True)

        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = (
            Order.objects.filter(id=order_id, user=request.user)
            .prefetch_related("items__product")
            .first()
        )

        if not order:
            return Response({"detail": "Not found"}, status=404)

        serializer = OrderDetailSerializer(order)

        return Response(serializer.data)


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = Order.objects.filter(id=order_id, user=request.user).first()

        if not order:
            return Response({"detail": "Order not found"}, status=404)

        if order.status != "pending":
            return Response({"detail": "Cannot cancel this order"}, status=400)

        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

            item.cancel()

        return Response({"message": "Order cancelled"})


class VendorSalesView(APIView):
    permission_classes = [IsAuthenticated, IsVendorOwner]

    def get(self, request, id):
        vendor = Vendor.objects.filter(id=id, user=request.user).first()

        if not vendor:
            return Response({"detail": "Vendor not found"}, status=404)

        items = OrderItem.objects.filter(
            product__vendor=vendor, order__status="confirmed"
        )

        data = items.values("product__id", "product__name").annotate(
            total_sold=Sum("quantity")
        )

        return Response(data)


class UpdateOrderItemStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        serializer = UpdateOrderItemStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]

        item = (
            OrderItem.objects.select_related("product__vendor", "order")
            .filter(id=item_id)
            .first()
        )

        if not item:
            return Response({"detail": "Order item not found"}, status=404)

        user = request.user

        if user.is_staff:
            item.status = new_status
            item.save()

            return Response({"message": "Status updated", "status": item.status})

        if item.order.user == user:
            if (
                item.status == OrderItem.Status.PENDING
                and new_status == OrderItem.Status.CANCELLED
            ):
                product = item.product
                product.stock += item.quantity
                product.save()

                item.cancel()

                return Response({"message": "Item cancelled", "status": item.status})

            return Response({"detail": "You cannot update this status"}, status=403)

        vendor = Vendor.objects.filter(user=user, id=item.product.vendor_id).first()

        if vendor:
            if (
                item.status == OrderItem.Status.PENDING
                and new_status == OrderItem.Status.CONFIRMED
            ):
                item.confirm()

            elif (
                item.status == OrderItem.Status.CONFIRMED
                and new_status == OrderItem.Status.SHIPPED
            ):
                item.ship()

            elif (
                item.status == OrderItem.Status.SHIPPED
                and new_status == OrderItem.Status.DELIVERED
            ):
                item.deliver()

            else:
                return Response({"detail": "Invalid status transition"}, status=400)

            return Response({"message": "Status updated", "status": item.status})

        return Response({"detail": "Permission denied"}, status=403)
