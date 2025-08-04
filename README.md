# 🚀 Lang‑Graph

A graph‑based orchestration framework for building **long‑running, stateful AI agents**, complete with **durable execution**, **human‑in‑the‑loop (HITL)** control, memory persistence, and observability through LangSmith.

---

## 📌 Overview
LangGraph lets you create workflows as **graphs** of computation steps — LLM calls, tools, or Python functions — connected with conditional or cyclic edges.

This project demonstrates:
- 💾 **Durable execution & checkpoints** to resume workflows after interruptions  
- 👥 **Human‑in‑the‑loop control** for interactive decision-making mid‑workflow  
- 🧠 **Memory support** via `MemorySaver`  
- 🔍 **LangSmith observability** for tracing and debugging agent runs  

---

## 🛠 Installation
```bash
  pip install -U langgraph langchain-openai langchain-anthropic python-dotenv

```
(Optional) Install LangSmith for tracing:
```bash
  pip install langsmith


```
## Create a .env file in the root directory and add your API keys:
```bash
  OPENAI_API_KEY=your_openai_key
  LANGSMITH_API_KEY=your_langsmith_key
```

## ⚡ Quickstart
You can start by creating a simple LangGraph workflow:

1. Define a state schema (data structure for passing information between nodes).

2. Create computation nodes (LLM calls, tools, or functions).

3. Connect nodes with edges (including conditional or looping flows).

4. Use a checkpointer like MemorySaver for persistence.

## 👥 Human‑in‑the‑Loop (HITL)

The HITL examples (8_HITL.py) show how you can pause a running graph and request human input before continuing.

## 📂 Project Structure


### ├── 1_simple_graph.ipynb
### ├── 2_add_tool_node.ipynb
### ├── 3_state_memory.ipynb
### ├── 4_agent_with_tool.ipynb
### ├── 5_multi_tool_agent.ipynb
### ├── 6_agent_with_checkpointer.ipynb
### ├── 7_langsmith_tracing.ipynb
### ├── 8_HITL.py
### ├── 9_HITL_LangSmith.py
### ├── main.py
### ├── pyproject.toml
### ├── .env.example
### └── README.md

## 📖 Why Use LangGraph?
✅ Flexible graph‑based orchestration — supports loops, branching, subgraphs

💾 Persistent checkpoints — recover from failures or resume long tasks

👥 HITL — pause execution and await human decisions mid‑flow

🔍 Tracing with LangSmith — complete visibility into runs and states

## 📄 License
Distributed under the MIT License.

## ⚙️ Contribution Tips
Define clear state schemas and runtime contexts.

Add examples for branching, tool-calling, and resume points.

Use LangSmith for observability during development.

Test persistence and HITL flows with multiple runs.
