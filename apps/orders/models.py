from django.db import models
from django.conf import settings


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def status(self):

        statuses = self.items.values_list("status", flat=True)

        if not statuses:
            return "pending"

        statuses = list(statuses)

        if all(s == OrderItem.Status.DELIVERED for s in statuses):
            return "delivered"

        if all(s == OrderItem.Status.CANCELLED for s in statuses):
            return "cancelled"

        if any(s == OrderItem.Status.SHIPPED for s in statuses):
            return "shipped"

        if any(s == OrderItem.Status.CONFIRMED for s in statuses):
            return "confirmed"

        return "pending"

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending"
        CONFIRMED = "confirmed"
        SHIPPED = "shipped"
        DELIVERED = "delivered"
        CANCELLED = "cancelled"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def confirm(self):
        self.status = self.Status.CONFIRMED
        self.save()

    def ship(self):
        self.status = self.Status.SHIPPED
        self.save()

    def deliver(self):
        self.status = self.Status.DELIVERED
        self.save()

    def cancel(self):
        self.status = self.Status.CANCELLED
        self.save()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
