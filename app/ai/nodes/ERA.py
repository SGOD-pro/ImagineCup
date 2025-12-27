from app.ai.state import ClinicalGraphState
from app.ai.llm import NvidiaLLM
from app.ai.vector_serarch import similarity_search
'''RAG Evidence Retrieval

     Pulls from WHO / CDC vectors
     Output = citations + snippets
'''


# def evidence_retrieval(state: ClinicalGraphState) -> ClinicalGraphState:
#      # extract structure
#      # llm = NVDIALLM(model_name="nvidia/nvidia-nemotron-nano-9b-v2", temp=0.25)
#      # response = llm.invoke("")
#      # state["structured_symptoms"] = {}
#      # return state

async def evidence_retrieval(state: ClinicalGraphState) -> ClinicalGraphState:
     structured = state.get("structured_symptoms")

     if not structured:
          state["evidence"] = []
          return state

     query_parts = structured["chief_complaints"]

     if structured.get("red_flags"):
          query_parts += structured["red_flags"]

     query = " ".join(query_parts)

     docs = await similarity_search(query, limit=5)

     evidence = []
     for doc, score in docs:
          evidence.append({
               "source": doc.metadata.get("source", "unknown"),
               "title": doc.metadata.get("title", ""),
               "excerpt": doc.page_content[:500],
               "url": doc.metadata.get("url")
          })

     state["evidence"] = evidence
     return state

