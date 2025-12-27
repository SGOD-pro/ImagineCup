from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from app.config import settings
embding_model = NVIDIAEmbeddings(
                    model="nvidia/llama-3.2-nemoretriever-300m-embed-v2", 
                    api_key=settings.NIM_API, 
                    truncate="NONE", 
                )

client = QdrantClient(url=settings.QDRANT_URL,api_key=settings.QDRANT_KEY,)


if not client.collection_exists("clinic"):
    client.create_collection(
        collection_name="test",
        vectors_config=VectorParams(size=4096, distance=Distance.COSINE)
    )

vector_store = QdrantVectorStore(
    client=client,
    collection_name="test",
    embedding=embding_model,
)