from django.urls import path

from .views import (
    AddToCartView,
    RemoveFromCartView,
    UpdateCartQuantityView,
    CartDetailView,
)

urlpatterns = [
    path("cart/add/", AddToCartView.as_view(), name="cart-add"),
    path("cart/remove/", RemoveFromCartView.as_view(), name="cart-remove"),
    path("cart/update/", UpdateCartQuantityView.as_view(), name="cart-update"),
    path("cart/", CartDetailView.as_view(), name="cart-detail"),
]
