from langgraph.graph import StateGraph, MessagesState, START, END
from app.ai.state import ClinicalGraphState
from app.ai.nodes import triage_agent,reasoning_agent,evidence_retrieval,ssa_node


def build_clinical_graph():
    graph = StateGraph(ClinicalGraphState)

    graph.add_node("ssa", ssa_node)#FIXME: labs reference_range contains some worng values correct them by male,female/children
    graph.add_node("evidence", evidence_retrieval)
    graph.add_node("reasoning", reasoning_agent)
    graph.add_node("triage", triage_agent)

    graph.add_edge(START, "ssa")
    graph.add_edge("ssa", "evidence")
    graph.add_edge("evidence", "reasoning")
    graph.add_edge("reasoning", "triage")
#   graph.add_edge("triage_agent", "guardrail")
    
    graph.add_edge("triage", END)

    return graph.compile()


'''
Retry Policy->

graph.add_node(
    "ssa_node", 
    ssa_node,
    retry_policy=RetryPolicy(
        max_attempts=4,           # 1 initial + 3 retries
        initial_interval=2.0,     # Start with 2s delay
        backoff_factor=2.0,       # Exponential: 2s → 4s → 8s
        retry_on=should_retry_ssa # Custom retry condition
    )
)
'''