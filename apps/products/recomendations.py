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

        products = Product.objects.filter(id__in=product_ids)

        product_map = {p.id: p for p in products}

        ordered_products = [
            product_map[pid]
            for pid in product_ids
            if pid in product_map
        ]

        return ordered_products
    
    user_vector = UserVector.objects.filter(user=user).first()
    
    if not user_vector:
        return trending_products()

    results = client.query_points(
        collection_name="products",
        query=user_vector.vector,
        limit=50
    )
    product_ids = [r.id for r in results]
    products = Product.objects.filter(id__in=product_ids)
    product_map = {p.id: p for p in products}

    ranked = rank_results(results, product_map)

    top_ranked = ranked[:20]

    final_product_ids = [p.id for score, p in top_ranked]

    ordered_products = [
        product_map[pid]
        for pid in final_product_ids
        if pid in product_map
    ]

    redis_client.setex(cache_key, CACHE_TTL, json.dumps(final_product_ids))

    return ordered_products


def rank_results(results, product_map):
    ranked = []

    for r in results:
        product = product_map.get(r.id)

        if not product:
            continue

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