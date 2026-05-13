from django.db import models
from django.contrib.auth.models import User
from apps.orders.models import Order


class Invoice(models.Model):
    STATUS = (
        ("pending", "pending"),
        ("paid", "paid"),
        ("cancelled", "cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)