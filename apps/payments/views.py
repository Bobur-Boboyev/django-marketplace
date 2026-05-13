from paytechuz.integrations.django.views import BasePaymeWebhookView

from apps.payments.models import Invoice
from apps.orders.models import Order
from apps.vendors.services import distribute_payment


class PaymeWebhookView(BasePaymeWebhookView):
    def successfully_payment(self, params, transaction):

        invoice = Invoice.objects.get(id=transaction.account_id)

        invoice.status = "paid"
        invoice.save()

        order = invoice.order

        order.is_paid = True
        order.save()

        distribute_payment(order.id)
