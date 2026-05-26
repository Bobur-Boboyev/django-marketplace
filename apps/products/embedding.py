from sentence_transformers import SentenceTransformer
import numpy as np

from apps.events.models import UserEvent

_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model

def create_embedding(text):
    model = get_model()
    vector = model.encode(text)

    return vector.tolist()


def build_user_vector(user):
    events = UserEvent.objects.filter(user=user)

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
        return None

    return np.average(vectors, axis=0, weights=weights).tolist()