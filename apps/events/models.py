from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product


User = get_user_model()

class UserEvent(models.Model):
    VIEW = "view"
    CLICK = "click"
    CART = "cart"
    PURCHASE = "purchase"

    EVENT_TYPES = [
        (VIEW, VIEW),
        (CLICK, CLICK),
        (CART, CART),
        (PURCHASE, PURCHASE),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)