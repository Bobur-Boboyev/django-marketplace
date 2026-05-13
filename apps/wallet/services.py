from django.db import transaction
from django.utils import timezone

from .models import (
    Wallet,
    WalletTransaction,
    WithdrawalRequest
)


class WalletService:


    @staticmethod
    @transaction.atomic
    def credit_wallet(vendor_id, amount, reference):
        wallet, _ = Wallet.objects.get_or_create(vendor_id=vendor_id)

        wallet.balance += amount
        wallet.save()

        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            type="credit",
            reference=reference
        )

    @staticmethod
    @transaction.atomic
    def create_withdrawal(vendor, amount, card_number):

        wallet = Wallet.objects.select_for_update().get(
            vendor=vendor
        )

        if wallet.balance < amount:
            raise Exception("Insufficient balance")

        withdrawal = WithdrawalRequest.objects.create(
            vendor=vendor,
            amount=amount,
            card_number=card_number
        )

        return withdrawal

    @staticmethod
    @transaction.atomic
    def approve_withdrawal(withdrawal_id):

        withdrawal = WithdrawalRequest.objects.select_for_update().get(
            id=withdrawal_id
        )

        if withdrawal.status != "pending":
            raise Exception("Only pending withdrawals can be approved")

        wallet = Wallet.objects.select_for_update().get(
            vendor=withdrawal.vendor
        )

        if wallet.balance < withdrawal.amount:
            raise Exception("Insufficient balance")

        withdrawal.status = "approved"
        withdrawal.approved_at = timezone.now()
        withdrawal.save()

        return withdrawal
    
    @staticmethod
    @transaction.atomic
    def reject_withdrawal(
        withdrawal_id,
        reason
    ):

        withdrawal = WithdrawalRequest.objects.select_for_update().get(
            id=withdrawal_id
        )

        if withdrawal.status != "pending":
            raise Exception("Only pending withdrawals can be rejected")

        withdrawal.status = "rejected"
        withdrawal.rejection_reason = reason

        withdrawal.save()

        return withdrawal
    
    @staticmethod
    @transaction.atomic
    def mark_as_paid(withdrawal_id):

        withdrawal = WithdrawalRequest.objects.select_for_update().get(
            id=withdrawal_id
        )

        if withdrawal.status != "approved":
            raise Exception("Withdrawal must be approved first")

        wallet = Wallet.objects.select_for_update().get(
            vendor=withdrawal.vendor
        )

        if wallet.balance < withdrawal.amount:
            raise Exception("Insufficient balance")

        wallet.balance -= withdrawal.amount
        wallet.save()

        WalletTransaction.objects.create(
            wallet=wallet,
            amount=withdrawal.amount,
            type="debit",
            reference=f"withdrawal:{withdrawal.id}"
        )

        withdrawal.status = "paid"
        withdrawal.paid_at = timezone.now()

        withdrawal.save()

        return withdrawal