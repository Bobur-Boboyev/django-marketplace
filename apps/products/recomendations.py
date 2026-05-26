from datetime import timezone
import json

from django.db.models import Case, When, Count

from apps.products.utils import recency_score
from apps.users.models import UserVector

from .models import Product
from .embedding import create_embedding
from .qdrant import client
from .redis import redis_client
from .embedding import build_user_vector

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
        product_ids = json.loads(cached)

        preserved_order = Case(*[When(id=pid, then=pos) for pos, pid in enumerate(product_ids)])
        return list(Product.objects.filter(id__in=product_ids).order_by(preserved_order))

    user_vector = UserVector.objects.filter(user=user).first()

    if not user_vector:
        return []

    results = client.query_points(
        collection_name="products",
        query=user_vector.vector,
        limit=50
    )
    ranked = rank_results(results)
    results = [product for score, product in ranked[:20]]

    redis_client.setex(cache_key, CACHE_TTL, json.dumps([r.id for r in results]))

    return results


def rank_results(results):
    ranked = []

    for r in results:
        product = Product.objects.get(id=r.id)

        similarity_score = r.score
        popularity_score = product.popularity_score
        recency = recency_score(product)

        final_score = similarity_score * 0.5 + popularity_score * 0.3 + recency * 0.2

        ranked.append((final_score, product))

    ranked.sort(key=lambda x: x[0], reverse=True)

    return ranked


def trending_products():
    since = timezone.now() - timezone.timedelta(hours=7)

    return Product.objects.filter(events__created_at__gte=since).annotate(
        score=Count("events")
    ).order_by("-popularity_score")