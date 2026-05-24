from .models import Product
from .embedding import create_embedding
from .qdrant import client
from django.core.exceptions import ObjectDoesNotExist



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