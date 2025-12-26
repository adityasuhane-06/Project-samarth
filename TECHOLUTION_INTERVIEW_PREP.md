# 🎯 Techolution Gen AI/ML Interview Prep
## LangChain + RAG + LangGraph Quick Reference

**Interview Date:** Tuesday (Dec 31, 2025)

---

## ✅ What You Now Have in Project Samarth

### 1. LangChain Integration (`src/services/langchain_ai.py`)
- **LCEL (LangChain Expression Language)** - Clean pipeline composition
- **Prompt Templates** - Maintainable, reusable prompts
- **Output Parsers** - Structured JSON extraction
- **Two-model architecture** refactored with LangChain

### 2. RAG System (`src/services/rag_service.py`)
- **ChromaDB** - Vector database for semantic search (Cloud + Local)
- **HuggingFace Embeddings** - `all-MiniLM-L6-v2` for text vectors
- **16 agricultural knowledge documents** embedded
- **Similarity search** with relevance scoring

### 3. 🆕 LangGraph Agentic Workflow (`src/services/langgraph_agent.py`)
- **StateGraph** - Typed state machine for multi-step reasoning
- **Tool Binding** - LLM autonomously decides which tools to call
- **Conditional Routing** - Agent loops until answer is complete
- **4 Agricultural Tools** - APEDA, Crop, Rainfall, Knowledge Base

---

## 🗣️ Key Interview Talking Points

### "Tell me about your LangChain implementation"

> "I refactored my agricultural Q&A system to use LangChain. I'm using LCEL - LangChain Expression Language - to compose clean pipelines. My QueryRouter uses a PromptTemplate connected to Gemini 2.5-flash, followed by a StrOutputParser. The chain syntax `prompt | llm | parser` makes the code more maintainable and easier to extend."

### "Explain your RAG architecture"

> "I built a RAG system using ChromaDB as my vector store. I embedded 16 agricultural knowledge documents using HuggingFace's all-MiniLM-L6-v2 model - it's fast and runs locally without API limits. When a user asks a question, I:
> 1. Convert query to vector using the same embedding model
> 2. Perform similarity search in ChromaDB (k=3 results)
> 3. Pass retrieved context + original question to Gemini
> 4. Generate a grounded answer with citations"

### 🆕 "How does your LangGraph agent work?"

> "I built a true agentic system using LangGraph. It has:
> 1. **Typed State** - An `AgentState` TypedDict that tracks question, messages, collected data, and sources used
> 2. **Tool Binding** - Four tools the agent can call: APEDA production, crop data, rainfall, and RAG search
> 3. **Conditional Routing** - After each LLM call, I check if it wants to call tools or synthesize an answer
> 4. **Multi-step Reasoning** - The agent can loop through tools multiple times before final answer
>
> For example, when asked 'Compare rice production with rainfall in 2020', the agent autonomously decided to call TWO tools - fetch_apeda_production AND fetch_rainfall_data - then synthesized both results."

### 🆕 "What's the difference between chains and agents?"

> "**Chains** are linear: prompt → LLM → output. The flow is predetermined.
> 
> **Agents** are dynamic: the LLM decides which tools to call and when. It's a loop where the agent reasons, acts, observes, and repeats until done.
>
> My LangGraph implementation uses a StateGraph where:
> - `agent` node does reasoning
> - `tools` node executes tool calls  
> - `synthesize` node generates final answer
> - Conditional edges route based on LLM's decisions"

---

## 💡 Technical Deep Dives (If Asked)

### LCEL Pipeline (LangChain Expression Language)
```python
# My actual code pattern:
chain = self.prompt | self.llm | StrOutputParser()
result = chain.invoke({"question": user_query})
```

### RAG Search Flow
```python
# 1. Embed query
query_vector = embeddings.embed_query(question)

# 2. Similarity search in ChromaDB
results = vector_store.similarity_search_with_score(query, k=3)

# 3. Build context and generate
context = "\n".join([doc.page_content for doc, score in results])
answer = llm.invoke(f"Context: {context}\nQuestion: {question}")
```

### 🆕 LangGraph State Machine
```python
# My AgentState - the "memory" of the agent
class AgentState(TypedDict):
    question: str                    # User's question
    messages: List[Any]              # Conversation history
    collected_data: dict             # Data from tools
    sources_used: List[str]          # Which sources answered
    step_count: int                  # Prevent infinite loops

# Graph structure
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)       # LLM reasoning
workflow.add_node("tools", tool_node)        # Execute tools
workflow.add_node("synthesize", synth_node)  # Final answer

# Conditional routing - THIS IS THE AGENTIC PART
workflow.add_conditional_edges("agent", should_continue, 
    {"tools": "tools", "synthesize": "synthesize"})
```

---

## ❓ Likely Interview Questions

### Q1: "What is RAG and why is it useful?"
> "Retrieval Augmented Generation. It grounds LLM responses in actual data by retrieving relevant documents before generation. Benefits:
> - Reduces hallucination
> - Keeps answers current (knowledge base can be updated)
> - Enables citation of sources"

### Q2: "Difference between LangChain and LangGraph?"
> "LangChain is for building chains - linear pipelines of operations. LangGraph is for building agents - cyclic graphs with state machines, conditionals, and loops. I use LangChain for simple Q&A chains, and LangGraph for my multi-tool agricultural agent."

### 🆕 Q3: "How does your agent decide which tools to use?"
> "The LLM has tool descriptions bound to it. When I call `llm.bind_tools(tools)`, it can output `tool_calls` in its response. My routing logic checks if `tool_calls` exists - if yes, execute them and loop back to agent. The LLM autonomously figures out from the question which tools are relevant."

### 🆕 Q4: "How do you prevent infinite loops in your agent?"
> "Two safeguards:
> 1. `step_count` in state - if it exceeds 5, force synthesize
> 2. Conditional routing always ends at `synthesize` or `END` node
> The agent can't get stuck because every path eventually terminates."

### Q5: "How would you scale this RAG system?"
> "For production scaling:
> - Move to Chroma Cloud or Pinecone for managed vector DB ✅ (already done!)
> - Add metadata filtering for faster retrieval
> - Implement hybrid search (keyword + semantic)
> - Add re-ranking layer before generation
> - Cache frequently asked questions"

---

## 🏃 Run Before Interview

```bash
# Verify LangChain + RAG
cd src
python test_langchain_rag.py

# Test LangGraph Agent
python -c "import sys; sys.path.insert(0, '.'); from services.langgraph_agent import get_agent; agent = get_agent(); result = agent.query('What is rice production in Punjab?'); print(result['answer'])"
```

---

## 📁 Files Added

| File | Purpose |
|------|---------|
| `src/services/langchain_ai.py` | LangChain-powered router & processor |
| `src/services/rag_service.py` | RAG with ChromaDB + HuggingFace embeddings |
| `src/services/langgraph_agent.py` | 🆕 **LangGraph agentic workflow** |
| `src/test_langchain_rag.py` | Test suite for verification |
| `chroma_db/` | Local vector database storage |

---

## 🎤 One-Liner Descriptions

- **LangChain**: "Framework for building LLM applications through composable chains"
- **RAG**: "Retrieval Augmented Generation - ground LLM in retrieved documents"
- **ChromaDB**: "Open-source embedding database for vector similarity search"
- **LCEL**: "LangChain Expression Language - pipe syntax for chaining operations"
- **LangGraph**: "Framework for building stateful, multi-step AI agents"
- **Agentic AI**: "LLM autonomously decides actions and tool usage"

---

## ✨ Updated Resume Bullet Points

```
• Refactored AI pipeline using LangChain framework with LCEL 
  (LangChain Expression Language) for clean, maintainable 
  prompt templates and chain composition.

• Implemented RAG (Retrieval Augmented Generation) system using 
  ChromaDB vector database and HuggingFace embeddings, enabling 
  semantic search over 16 agricultural knowledge documents.

• Built agentic workflow using LangGraph with autonomous tool 
  selection, multi-step reasoning, and conditional state routing
  for complex agricultural queries across multiple data sources.
```

---

**Good luck with Techolution! 🚀**
