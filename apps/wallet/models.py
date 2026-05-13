from django.db import models
from apps.vendors.models import Vendor


class Wallet(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet({self.vendor_id})"

class WalletTransaction(models.Model):
    class Type(models.TextChoices):
        CREDIT = "credit"
        DEBIT = "debit"

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=Type.choices)

    reference = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)