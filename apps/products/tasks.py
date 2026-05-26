import numpy as np

from celery import shared_task
from django.db import models

from events.models import UserEvent
from apps.users.models import UserVector
from .models import Product

from .embedding import create_embedding
from .qdrant import client


@shared_task
def build_user_vector_task(user_id):
    events = UserEvent.objects.filter(user_id=user_id).select_related("product")

    vectors = []
    weights = []

    for e in events:
        text = f"{e.product.name} {e.product.description}"

        v = create_embedding(text)

        vectors.append(v)

        if e.event_type == "view":
            weights.append(1)
        elif e.event_type == "click":
            weights.append(2)
        elif e.event_type == "cart":
            weights.append(5)
        else:
            weights.append(10)

    if not vectors:
        return

    user_vector, created = UserVector.objects.get_or_create(user_id=user_id)
    user_vector.vector = np.average(vectors, axis=0, weights=weights).tolist()
    user_vector.save()


@shared_task
def recompute_popularity():
    products = Product.objects.annotate(
        popularity_score=models.Count("events")
    )

    for product in products:
        score = UserEvent.objects.filter(
            product=product
        ).count()

        product.popularity_score = score

        product.save()


@shared_task
def index_product_to_qdrant(product_id):
    product = Product.objects.get(id=product_id)
    text = f"{product.name} {product.description}"

    vector = create_embedding(text)

    client.upsert(
        collection_name="products",
        points=[
            {
                "id": product.id,
                "vector": vector,
                "payload": {
                    "name": product.name,
                    "category": product.category
                }
            }
        ]
    )