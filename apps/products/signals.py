from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product
from .tasks import index_product_to_qdrant


@receiver(post_save, sender=Product)
def product_created(sender, instance, created, **kwargs):

    if created:
        index_product_to_qdrant.delay(instance.id)