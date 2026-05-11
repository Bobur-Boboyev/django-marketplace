from django.urls import path

from .views import ProductListCreateView

urlpatterns = [
    path('api/products/', ProductListCreateView.as_view(), name='product_list_create'),
]