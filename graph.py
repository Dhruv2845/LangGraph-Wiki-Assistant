from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import classify, respond_search, respond_greetings
builder = StateGraph(AgentState)

builder.add_node("classify", classify)
builder.add_node("agent", respond_search)
#builder.add_node("tools", ToolNode(tools))
builder.add_node("simple_greet", respond_greetings)

builder.add_edge(START, "classify")
def route_classification(state:AgentState):
    if state.classification == "greetings":
        return "simple_greet"
    return "agent"

builder.add_conditional_edges(
    "classify",
    route_classification,{
        "simple_greet":"simple_greet",
        "agent":"agent"
    }
)

builder.add_edge("agent", END)
builder.add_edge("simple_greet", END)
app = builder.compile()