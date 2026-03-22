from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    raw_text: str
    retrieved_context: List[str]
    analysis: str
    risk_score: int

def retrieve_node(state: AgentState):
    # এখানে VectorManager থেকে প্রাসঙ্গিক তথ্য খুঁজে বের করবে (RAG)
    return {"retrieved_context": ["Context from Vector DB..."]}

def analysis_node(state: AgentState):
    # এখানে জেমিনি বা ক্লড এনালাইসিস করবে
    return {"analysis": "Professional Lease Report based on RAG"}

# গ্রাফ বিল্ড করা
workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("analyze", analysis_node)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "analyze")
workflow.add_edge("analyze", END)
app_graph = workflow.compile()