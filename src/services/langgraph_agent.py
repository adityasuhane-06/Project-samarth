"""
LangGraph Agentic Workflow for Agricultural Q&A
This creates a TRUE agentic system where the LLM autonomously decides which tools to call.

Key Interview Points:
- State machine with typed state
- Conditional routing based on LLM decisions
- Tool nodes that execute data fetches
- Multi-step reasoning with memory
"""
import json
import operator
from typing import TypedDict, Annotated, List, Literal, Optional, Any
from dataclasses import dataclass

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from config.settings import settings


# ============================================================================
# STATE DEFINITION
# ============================================================================

class AgentState(TypedDict):
    """
    State that flows through the graph.
    This is the "memory" of the agent across steps.
    """
    # The user's original question
    question: str
    
    # Messages for conversation history
    messages: Annotated[List[Any], operator.add]
    
    # Data collected from tools
    collected_data: dict
    
    # Which data sources have been queried
    sources_used: List[str]
    
    # Final answer
    final_answer: Optional[str]
    
    # Number of reasoning steps (to prevent infinite loops)
    step_count: int


# ============================================================================
# TOOLS (What the agent can call)
# ============================================================================

@tool
def fetch_apeda_production(state: str = None, year: str = None, category: str = "Agri") -> dict:
    """
    Fetch agricultural production data from APEDA (2019-2024).
    Use for recent state-level crop, fruit, vegetable, livestock production.
    
    Args:
        state: Indian state name (e.g., "Punjab", "Maharashtra")
        year: Year like "2023" or "2023-24"
        category: One of Agri, Fruits, Vegetables, Spices, LiveStock, Floriculture
    """
    # Simulated response for demo (in production, call actual API)
    return {
        "source": "apeda_production",
        "years_available": "2019-2024",
        "data": [
            {"state": state or "All India", "category": category, "year": year or "2023-24", 
             "production_tonnes": 125000, "export_value_usd": 45000000}
        ],
        "note": f"APEDA production data for {category} in {state or 'All India'}"
    }


@tool
def fetch_crop_production(district: str = None, crop: str = None, year: str = None) -> dict:
    """
    Fetch district-level crop production data (2013-2015).
    Use for detailed district-wise crop statistics, area, yield data.
    
    Args:
        district: District name
        crop: Crop name (e.g., "rice", "wheat", "cotton")
        year: Year (2013, 2014, or 2015)
    """
    return {
        "source": "crop_production",
        "years_available": "2013-2015",
        "data": [
            {"district": district or "Sample District", "crop": crop or "rice", 
             "year": year or "2014", "area_hectares": 50000, "production_tonnes": 120000, 
             "yield_kg_per_hectare": 2400}
        ],
        "note": f"District crop production for {crop or 'rice'}"
    }


@tool
def fetch_rainfall_data(state: str = None, year: str = None, rainfall_type: str = "historical") -> dict:
    """
    Fetch rainfall data - historical (1901-2015) or daily (2019-2024).
    Use for weather patterns, monsoon analysis, climate trends.
    
    Args:
        state: Indian state name
        year: Year or year range
        rainfall_type: "historical" for 1901-2015, "daily" for 2019-2024
    """
    if rainfall_type == "historical":
        return {
            "source": "historical_rainfall",
            "years_available": "1901-2015",
            "data": [
                {"state": state or "Maharashtra", "year": year or "1950", 
                 "annual_rainfall_mm": 1200, "monsoon_rainfall_mm": 950}
            ],
            "note": f"Historical rainfall data for {state or 'India'}"
        }
    else:
        return {
            "source": "daily_rainfall", 
            "years_available": "2019-2024",
            "data": [
                {"state": state or "Maharashtra", "year": year or "2023",
                 "total_rainfall_mm": 1150, "rainy_days": 65}
            ],
            "note": f"Recent daily rainfall data for {state or 'India'}"
        }


@tool
def search_knowledge_base(query: str) -> dict:
    """
    Search the agricultural knowledge base using RAG.
    Use for general agricultural information, crop details, regional specialties.
    
    Args:
        query: Natural language search query
    """
    try:
        from services.rag_service import get_rag_service
        rag = get_rag_service(use_cloud=False)  # Use local for speed
        results = rag.search(query, k=2)
        return {
            "source": "knowledge_base",
            "results": [{"content": r["content"][:200], "type": r["metadata"].get("source")} 
                       for r in results]
        }
    except Exception as e:
        return {"source": "knowledge_base", "error": str(e), "results": []}


@tool
def web_search(query: str) -> dict:
    """
    Search the web for real-time agricultural information using Google.
    Use for current news, latest policies, recent market prices, export regulations.
    
    Args:
        query: Search query (e.g., "mango export policy 2024", "rice prices today")
    """
    import os
    try:
        from googleapiclient.discovery import build
        
        api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        cx = os.getenv("GOOGLE_SEARCH_CX")
        
        if not api_key or not cx:
            return {"source": "web_search", "error": "Google Search API not configured", "results": []}
        
        service = build('customsearch', 'v1', developerKey=api_key)
        result = service.cse().list(q=query, cx=cx, num=3).execute()
        
        items = result.get('items', [])
        return {
            "source": "web_search",
            "query": query,
            "total_results": result.get('searchInformation', {}).get('totalResults', 0),
            "results": [
                {
                    "title": item.get('title', ''),
                    "snippet": item.get('snippet', ''),
                    "link": item.get('link', '')
                }
                for item in items[:3]
            ]
        }
    except Exception as e:
        return {"source": "web_search", "error": str(e), "results": []}


# List of all tools
ALL_TOOLS = [fetch_apeda_production, fetch_crop_production, fetch_rainfall_data, search_knowledge_base, web_search]


# ============================================================================
# AGENT NODES (Steps in the workflow)
# ============================================================================

def create_agent_node(tools: list):
    """Create the main agent reasoning node"""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.3
    ).bind_tools(tools)
    
    def agent_node(state: AgentState) -> dict:
        """
        The agent reasons about what to do next.
        It can either call tools or generate final answer.
        """
        print(f"DEBUG: Agent reasoning step {state.get('step_count', 0) + 1}")
        
        # Build system message
        system_msg = SystemMessage(content="""You are an agricultural data assistant with access to multiple data sources.

Available tools:
1. fetch_apeda_production - For recent (2019-2024) state-level production data
2. fetch_crop_production - For district-level crop data (2013-2015)
3. fetch_rainfall_data - For historical (1901-2015) or recent (2019-2024) rainfall
4. search_knowledge_base - For general agricultural knowledge from our database
5. web_search - For REAL-TIME web search: current news, latest policies, market prices, export regulations

IMPORTANT:
- Call relevant tools to gather data before answering
- You can call multiple tools if needed
- After gathering data, provide a comprehensive answer
- If you have enough data, generate the final answer directly""")
        
        # Get current messages
        messages = [system_msg] + state.get("messages", [])
        
        # Add context about collected data if any
        if state.get("collected_data"):
            context_msg = HumanMessage(content=f"Data collected so far: {json.dumps(state['collected_data'], indent=2)}")
            messages.append(context_msg)
        
        # Invoke LLM
        response = llm.invoke(messages)
        
        return {
            "messages": [response],
            "step_count": state.get("step_count", 0) + 1
        }
    
    return agent_node


def tool_executor_node(state: AgentState) -> dict:
    """Execute tools called by the agent"""
    
    last_message = state["messages"][-1]
    
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return {}
    
    collected_data = state.get("collected_data", {})
    sources_used = state.get("sources_used", [])
    tool_messages = []
    
    # Map tool names to functions
    tool_map = {t.name: t for t in ALL_TOOLS}
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        print(f"DEBUG: Executing tool '{tool_name}' with args: {tool_args}")
        
        if tool_name in tool_map:
            try:
                result = tool_map[tool_name].invoke(tool_args)
                collected_data[tool_name] = result
                sources_used.append(result.get("source", tool_name))
                
                tool_messages.append(
                    ToolMessage(content=json.dumps(result), tool_call_id=tool_call["id"])
                )
            except Exception as e:
                tool_messages.append(
                    ToolMessage(content=f"Error: {str(e)}", tool_call_id=tool_call["id"])
                )
    
    return {
        "messages": tool_messages,
        "collected_data": collected_data,
        "sources_used": list(set(sources_used))
    }


def synthesize_answer_node(state: AgentState) -> dict:
    """Generate final answer from collected data"""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.7
    )
    
    prompt = f"""Based on the following data, provide a comprehensive answer to the user's question.

Question: {state['question']}

Collected Data:
{json.dumps(state.get('collected_data', {}), indent=2)}

Sources Used: {', '.join(state.get('sources_used', []))}

Instructions:
1. Synthesize all collected data into a clear answer
2. Cite sources using [Source: source_name] format
3. Be specific with numbers and statistics
4. If data is limited, acknowledge what's available"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {
        "final_answer": response.content,
        "messages": [response]
    }


# ============================================================================
# ROUTING LOGIC
# ============================================================================

def should_continue(state: AgentState) -> Literal["tools", "synthesize", "end"]:
    """
    Decide next step based on agent's output.
    This is the key routing logic that makes it agentic!
    """
    # Prevent infinite loops
    if state.get("step_count", 0) >= 5:
        print("DEBUG: Max steps reached, synthesizing answer")
        return "synthesize"
    
    last_message = state["messages"][-1]
    
    # If agent called tools, execute them
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print(f"DEBUG: Agent wants to call {len(last_message.tool_calls)} tool(s)")
        return "tools"
    
    # If we have collected data, synthesize
    if state.get("collected_data"):
        print("DEBUG: Data collected, synthesizing answer")
        return "synthesize"
    
    # First step with no tools called - agent should call at least one tool
    # Force tool usage on first step if no data yet
    if state.get("step_count", 0) == 1 and not state.get("collected_data"):
        print("DEBUG: No tools called on first step, synthesizing with RAG")
        return "synthesize"
    
    # Otherwise, end (agent decided no tools needed)
    print("DEBUG: Agent done reasoning")
    return "synthesize"  # Always synthesize to get an answer


# ============================================================================
# BUILD THE GRAPH
# ============================================================================

def create_agricultural_agent():
    """
    Build the LangGraph workflow.
    
    Flow:
    START → agent → (tools → agent)* → synthesize → END
    
    The agent can loop through tools multiple times before final answer.
    """
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", create_agent_node(ALL_TOOLS))
    workflow.add_node("tools", tool_executor_node)
    workflow.add_node("synthesize", synthesize_answer_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges (the agentic part!)
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "synthesize": "synthesize",
            "end": END
        }
    )
    
    # Tools always go back to agent for next decision
    workflow.add_edge("tools", "agent")
    
    # Synthesize always ends
    workflow.add_edge("synthesize", END)
    
    # Compile
    return workflow.compile()


# ============================================================================
# MAIN INTERFACE
# ============================================================================

class AgriculturalAgent:
    """High-level interface to the LangGraph agent"""
    
    def __init__(self):
        print("DEBUG: Initializing Agricultural Agent with LangGraph...")
        self.graph = create_agricultural_agent()
        print("DEBUG: Agricultural Agent ready!")
    
    def query(self, question: str) -> dict:
        """
        Run an agentic query.
        The agent will autonomously decide which tools to use.
        """
        print(f"\n{'='*60}")
        print(f"AGENT QUERY: {question}")
        print('='*60)
        
        # Initial state
        initial_state = {
            "question": question,
            "messages": [HumanMessage(content=question)],
            "collected_data": {},
            "sources_used": [],
            "final_answer": None,
            "step_count": 0
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        return {
            "question": question,
            "answer": result.get("final_answer", "No answer generated"),
            "sources_used": result.get("sources_used", []),
            "data_collected": result.get("collected_data", {}),
            "reasoning_steps": result.get("step_count", 0)
        }


# ============================================================================
# SINGLETON
# ============================================================================

_agent: Optional[AgriculturalAgent] = None


def get_agent() -> AgriculturalAgent:
    """Get or create the agent singleton"""
    global _agent
    if _agent is None:
        _agent = AgriculturalAgent()
    return _agent


# ============================================================================
# QUICK TEST
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🤖"*30)
    print("\n  LANGGRAPH AGRICULTURAL AGENT TEST")
    print("\n" + "🤖"*30)
    
    agent = get_agent()
    
    # Test queries
    test_queries = [
        "What is rice production in Punjab?",
        "Compare rainfall in Maharashtra between 1950 and 2023",
        "Tell me about wheat cultivation in India"
    ]
    
    for query in test_queries:
        result = agent.query(query)
        print(f"\n📝 Answer: {result['answer'][:300]}...")
        print(f"📊 Sources: {result['sources_used']}")
        print(f"🔄 Steps: {result['reasoning_steps']}")
        print("-" * 60)
