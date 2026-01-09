from langgraph.graph import StateGraph, START, END
from app.ai.state import ClinicalGraphState
from app.ai.nodes import triage_agent,reasoning_agent,evidence_retrieval,ssa_node,reasoning_summary_node,guardrail_node,lab_flag_node,clinical_signal_node


def build_clinical_graph():
    graph = StateGraph(ClinicalGraphState)

    graph.add_node("ssa", ssa_node)
    graph.add_node("evidence", evidence_retrieval)
    graph.add_node("lab_flags", lab_flag_node)
    # 🔥 NEW — mandatory
    graph.add_node("clinical_signals", clinical_signal_node)
    
    graph.add_node("reasoning", reasoning_agent)
    graph.add_node("reasoning_summary", reasoning_summary_node)
    graph.add_node("triage", triage_agent)
    graph.add_node("guardrail", guardrail_node)

    graph.add_edge(START, "ssa")
    graph.add_edge("ssa", "evidence")
    graph.add_edge("evidence", "lab_flags")
    graph.add_edge("lab_flags", "clinical_signals")

    # reasoning is parallel, not controlling triage
    graph.add_edge("clinical_signals", "reasoning")
    graph.add_edge("reasoning", "reasoning_summary")
    graph.add_edge("reasoning_summary", "triage")
    graph.add_edge("triage", "guardrail")
    
    graph.add_edge("guardrail", END)

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