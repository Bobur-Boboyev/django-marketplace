from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer
from apps.products.models import Product


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related(
        'user',
        'product'
    )
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    