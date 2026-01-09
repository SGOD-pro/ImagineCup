from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from  app.core import settings
import os

NIM_API=settings.NIM_API if settings.NIM_API else os.environ.get("NIM_API")
QDRANT_URL=settings.QDRANT_URL if settings.QDRANT_URL else os.environ.get("QDRANT_URL")
QDRANT_KEY=settings.QDRANT_KEY if settings.QDRANT_KEY else os.environ.get("QDRANT_KEY")

COLLECTION = "clinical_signals"
# ---------------- EMBEDDINGS ----------------
embedding_model = NVIDIAEmbeddings(
    model="nvidia/llama-3.2-nemoretriever-300m-embed-v2",
    api_key=NIM_API,
    truncate="NONE",
)

# ---------------- QDRANT CLIENT ----------------
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_KEY,
)

# ---------------- COLLECTION ----------------
if not client.collection_exists(COLLECTION):
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=2048, distance=Distance.COSINE),
    )