from django.urls import path

from .views import (
    CreateOrderView,
    OrderHistoryView,
    OrderDetailView,
    CancelOrderView,
    VendorSalesView,
    UpdateOrderItemStatusView,
)

urlpatterns = [
    path("orders/create/", CreateOrderView.as_view(), name="create-order"),
    path("orders/history/", OrderHistoryView.as_view(), name="order-history"),
    path("orders/<int:order_id>/", OrderDetailView.as_view(), name="order-detail"),
    path(
        "orders/<int:order_id>/cancel/", CancelOrderView.as_view(), name="cancel-order"
    ),
    path("vendors/<int:id>/sales/", VendorSalesView.as_view(), name="vendor-sales"),
    path(
        "order-items/<int:item_id>/status/",
        UpdateOrderItemStatusView.as_view(),
        name="update-order-item-status",
    ),
]
