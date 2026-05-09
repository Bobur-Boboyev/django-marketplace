from django.urls import path
from .views import VendorListCreateView, VendorDetailAPIView

urlpatterns = [
    path('', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('<int:pk>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
]