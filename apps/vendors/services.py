from apps.orders.models import OrderItem
from apps.wallet.services import credit_wallet


def distribute_payment(order_id):

    items = OrderItem.objects.filter(order_id=order_id)

    vendor_map = {}

    for item in items:
        vendor_map[item.vendor_id] = vendor_map.get(item.vendor_id, 0) + item.price

    for vendor_id, amount in vendor_map.items():

        credit_wallet(
            vendor_id=vendor_id,
            amount=amount,
            reference=f"order_{order_id}"
        )