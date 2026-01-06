import json
import time
from typing import List
from langchain_core.documents import Document
from qdrant_client.models import Distance, VectorParams, PayloadSchemaType

from langchain_qdrant import QdrantVectorStore
from app.core.embeding_store import client,embedding_model,COLLECTION
import dotenv
dotenv.load_dotenv()
# ---------------- CONFIG ----------------

BATCH_SIZE = 25
SLEEP_SECONDS = 3
MAX_RETRIES = 4


# ---------------- COLLECTION ----------------
if not client.collection_exists(COLLECTION):
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=2048, distance=Distance.COSINE),
    )

# ---------------- PAYLOAD INDEXES ----------------
def safe_create_index(field: str):
    try:
        client.create_payload_index(
            collection_name=COLLECTION,
            field_name=field,
            field_schema=PayloadSchemaType.KEYWORD,
        )
    except Exception:
        pass  # index already exists

safe_create_index("metadata.signal_type")
safe_create_index("metadata.disease")
safe_create_index("metadata.symptoms")
safe_create_index("metadata.source")

# ---------------- VECTOR STORE ----------------
vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION,
    embedding=embedding_model,
)

# ---------------- INGESTION ----------------
def ingest_documents(records: List[dict]):
    docs: List[Document] = []

    for idx, ev in enumerate(records):
        try:
            # build embedding text safely
            embedding_text = ev.get("embedding_text")
            if not embedding_text:
                raise ValueError("Missing embedding_text")

            docs.append(
                Document(
                    page_content=embedding_text,
                    metadata=ev["metadata"],
                )
            )

            # batch insert
            if len(docs) >= BATCH_SIZE:
                _insert_batch(docs, idx)
                docs.clear()
                time.sleep(SLEEP_SECONDS)

        except Exception as e:
            print(f"[SKIP] Record {idx} failed: {e}")

    # final flush
    if docs:
        _insert_batch(docs, "FINAL")

def _insert_batch(docs: List[Document], idx):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            vector_store.add_documents(docs)
            print(f"[OK] Inserted batch ending at index {idx}")
            return
        except Exception as e:
            print(f"[RETRY {attempt}] Failed at index {idx}: {e}")
            time.sleep(SLEEP_SECONDS * attempt)

    print(f"[FATAL] Batch failed permanently at index {idx}")

# ---------------- MAIN ----------------
if __name__ == "__main__":
     with open("one_shot.json", "r", encoding="utf-8") as f:
          normalized_records = json.load(f)
     print("Okay, let's go!")
     sum=0
     for record in normalized_records:
          print(f"Starting ingestion of {len(record)} records...")
          # ingest_documents(record)
          # print("Ingestion completed.")
          sum=sum+len(record)
     print(sum)
