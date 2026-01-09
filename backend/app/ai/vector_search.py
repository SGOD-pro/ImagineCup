from app.core.embeding_store import client, embedding_model,COLLECTION
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import Filter, FieldCondition, MatchAny


vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION,
    embedding=embedding_model,
)

async def similarity_search(
    query: str,
    limit: int = 5,
    signal_types: list[str] | None = None,
):
    qdrant_filter = None

    if signal_types:
        qdrant_filter = Filter(
            must=[
                FieldCondition(
                    key="metadata.signal_type",
                    match=MatchAny(any=signal_types),
                )
            ]
        )

    docs_with_scores = await vector_store.asimilarity_search_with_score(
        query=query,
        k=limit * 2,
        filter=qdrant_filter,
    )

    return docs_with_scores[:limit]
