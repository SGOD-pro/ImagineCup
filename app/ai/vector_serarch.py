from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from app.config import settings
client = NVIDIAEmbeddings(
  model="nvidia/llama-3.2-nemoretriever-300m-embed-v2", 
  api_key=settings.NIM_API, 
  truncate="NONE", 
  )

embedding = client.embed_query("What is the capital of France?")
client = QdrantClient(":memory:")

vector_size = len(embedding)

if not client.collection_exists("test"):
    client.create_collection(
        collection_name="test",
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
vector_store = QdrantVectorStore(
    client=client,
    collection_name="test",
    embedding=embeddings,
)