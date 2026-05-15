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

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        self.update_product_rating(review.product)

    def perform_update(self, serializer):
        review = serializer.save()
        self.update_product_rating(review.product)

    def perform_destroy(self, instance):
        product = instance.product
        instance.delete()
        self.update_product_rating(product)

    def update_product_rating(self, product):
        reviews = product.reviews.all()

        average = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

        product.average_rating = round(average, 2)
        product.reviews_count = reviews.count()

        product.save(
            update_fields=[
                'average_rating',
                'reviews_count'
            ]
        )