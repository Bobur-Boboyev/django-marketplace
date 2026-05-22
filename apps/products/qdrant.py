from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams


client = QdrantClient(
    host="localhost",
    port=6333
)

client.recreate_collection(
    collection_name="products",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)