from .models import Product
from .embedding import create_embedding
from .qdrant import client

def index_products():
    products = Product.objects.all()

    points = []

    for product in products:

        text = f"""
        {product.name} {product.description}
        """

        vector = create_embedding(text)

        points.append({
            "id": product.id,
            "vector": vector,
            "payload": {
                "name": product.name
            }
        })

    client.upsert(
        collection_name="products",
        points=points
    )

    print("Indexed!")