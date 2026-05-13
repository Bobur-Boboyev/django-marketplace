from django.db import models
from django.conf import settings
from apps.orders.models import Order


class Invoice(models.Model):
    STATUS = (
        ("pending", "pending"),
        ("paid", "paid"),
        ("cancelled", "cancelled"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)