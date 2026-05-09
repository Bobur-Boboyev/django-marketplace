from django.urls import path
from .views import VendorListCreateView

urlpatterns = [
    path('', VendorListCreateView.as_view(), name='vendor-list-create'),
]