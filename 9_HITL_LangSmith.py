from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from langsmith import traceable


class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def get_stock_price(symbol: str) -> float:
    '''Return the current price of a stock given the stock symbol'''
    return {"MSFT": 200.3, "AAPL": 100.4, "AMZN": 150.0, "RIL": 87.6}.get(symbol, 0.0)

@tool
def buy_stocks(symbol: str, quantity: int, total_price: float) -> str:
    '''Buy stocks given the stock symbol and quantity'''
    decision = interrupt(f"Approve buying {quantity} {symbol} stocks for ${total_price:.2f}?")

    if decision == "yes":
        return f"You bought {quantity} shares of {symbol} for a total price of {total_price}"
    else:
        return "Buying declined."


tools = [get_stock_price, buy_stocks]

llm = init_chat_model("google_genai:gemini-2.0-flash")
llm_with_tools = llm.bind_tools(tools)

def chatbot_node(state: State):
    msg = llm_with_tools.invoke(state["messages"])
    return {"messages": [msg]}

memory = MemorySaver()
builder = StateGraph(State)
builder.add_node("chatbot", chatbot_node)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "buy_thread"}}
@traceable
@traceable
def call_graph(payload):
    if isinstance(payload, str):
        # Treat it like a normal query
        state = graph.invoke(
            {"messages": [{"role": "user", "content": payload}]},
            config=config
        )
    else:
        # Assume it's already in the correct format (e.g., Command object)
        state = graph.invoke(payload, config=config)

    return state["messages"][-1].content


# Step 1: user asks price
resp = call_graph("What is the current price of 10 MSFT stocks?")
print(resp)

# Step 2: user asks to buy
resp = call_graph("Buy 10 MSFT stocks at current price.")
print(resp)

decision = input("Approve (yes/no): ")
resp=call_graph(Command(resume=decision))
print(resp)


# @traceable
# def call_graph(query: str):
#     state = graph.invoke({"messages": [{"role": "user", "content": query}]}, config=config)
#     return state["messages"][-1].content
#
# @traceable
# def resume_graph(decision: str):
#     state = graph.invoke(Command(resume=decision), config=config)
#     return state["messages"][-1].content