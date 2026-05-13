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


class WithdrawalRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        PAID = "paid", "Paid"

    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="withdrawals"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    card_number = models.CharField(max_length=32)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    rejection_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.vendor.name} - {self.amount}"
