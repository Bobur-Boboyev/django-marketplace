from .models import Product
from .embedding import create_embedding
from .qdrant import client
from django.core.exceptions import ObjectDoesNotExist



def similar_products(product_id):
    try:
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:
        return []

    text = f"""
    {product.name}
    {product.description}
    {product.category}
    """

    vector = create_embedding(text)

    results = client.query_points(
        collection_name="products",
        query=vector,
        limit=5 
    )

    return results