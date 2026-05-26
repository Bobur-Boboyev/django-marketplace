from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams


client = QdrantClient(
    host="localhost",
    port=6333
)

COLLECTION_NAME = "products"


def init_qdrant():
    collections = client.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
