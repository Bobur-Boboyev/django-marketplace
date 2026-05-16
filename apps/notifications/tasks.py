from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def send_order_confirmation_email(
    self,
    user_email,
    order_id,
):
    try:
        subject = f"Order #{order_id} created"

        message = f"""
            Your order has been created successfully.

            Order ID: {order_id}

            We are waiting for vendors confirmation.
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )

    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def send_order_status_email(
    self,
    user_email,
    product_name,
    vendor_name,
    status,
):
    try:
        subject = f"{product_name} status updated"

        message = f"""
            Your product status has changed.

            Product: {product_name}

            Vendor: {vendor_name}

            New Status: {status}
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )

    except Exception as exc:
        raise self.retry(exc=exc)
