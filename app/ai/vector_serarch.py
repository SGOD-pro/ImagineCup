from app.core.embedings import client,embding_model
from langchain_qdrant import QdrantVectorStore

async def similarity_search(query: str, limit: int = 10):
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="test",
        embedding=embding_model,
    )
    # Over-fetch to compensate for duplicates
    docs_with_scores = await vector_store.asimilarity_search_with_score(
        query=query,
        k=limit * 2   
    )
    return docs_with_scores[:limit]