from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from eka.core import answer

class State(TypedDict):
    tenant: str
    question: str
    result: dict

def build_agent(store, provider=None):
    # A bounded read-only graph; no autonomous planning or write tools yet.
    graph = StateGraph(State)
    graph.add_node("knowledge_search", lambda state: {"result": (provider.respond(store, state["tenant"], state["question"]) if provider else answer(store, state["tenant"], state["question"]))})
    graph.add_edge(START, "knowledge_search")
    graph.add_edge("knowledge_search", END)
    return graph.compile()
