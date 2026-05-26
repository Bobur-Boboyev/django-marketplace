import math
from django.utils import timezone

def recency_score(product):
    hours = (
        timezone.now() - product.created_at
    ).total_seconds() / 3600

    return math.exp(-hours / 72)