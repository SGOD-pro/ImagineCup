from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from app.core import settings
embding_model = NVIDIAEmbeddings(
                    model="nvidia/llama-3.2-nemoretriever-300m-embed-v2", 
                    api_key=settings.NIM_API, 
                    truncate="NONE", 
                )

client = QdrantClient(url=settings.QDRANT_URL,api_key=settings.QDRANT_KEY,)

try:
     if not client.collection_exists("clinic"):
          client.create_collection(
               collection_name="test",
               vectors_config=VectorParams(size=2048, distance=Distance.COSINE)
          )
          
except Exception as e:
     print(e)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="test",
    embedding=embding_model,
)