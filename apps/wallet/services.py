from .models import Wallet, WalletTransaction


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