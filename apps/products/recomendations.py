import json

from .models import Product
from .embedding import create_embedding
from .qdrant import client
from .redis import redis_client

from apps.users.embedding import build_user_vector

CACHE_TTL = 300

def similar_products(product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return []

    stored = client.retrieve(
        collection_name="products",
        ids=[product.id]
    )

    if not stored:
        return []

    vector = stored[0].vector

    results = client.query_points(
        collection_name="products",
        query=vector,
        limit=6
    )
    results = [Product.objects.get(id=r.id) for r in results if r.id != product.id]

    return results


def recommend_for_user(user):
    cache_key = f"user_recommendations:{user.id}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    user_vector = build_user_vector(user)

    if not user_vector:
        return []

    results = client.query_points(
        collection_name="products",
        query=user_vector,
        limit=10
    )
    results = [Product.objects.get(id=r.id) for r in results]

    redis_client.setex(cache_key, CACHE_TTL, json.dumps([r.id for r in results]))

    return results