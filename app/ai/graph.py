from langgraph.graph import StateGraph, START, END
from app.ai.state import ClinicalGraphState
from app.ai.nodes import triage_agent,reasoning_agent,evidence_retrieval,ssa_node

graph = StateGraph(ClinicalGraphState)
graph.add_node(ssa_node)
graph.add_node(reasoning_agent)
graph.add_node(evidence_retrieval)
graph.add_node(triage_agent)
graph.add_edge(START, "ssa_node")
graph.add_edge("ssa_node", "evidence_retrieval")
graph.add_edge("evidence_retrieval", "reasoning_agent")
graph.add_edge("reasoning_agent", "triage_agent")
# graph.add_edge("triage_agent", "guardrail")
graph.add_edge("triage_agent", END)
graph = graph.compile()


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