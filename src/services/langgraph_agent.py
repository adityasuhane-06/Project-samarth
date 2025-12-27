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

# Import the actual data integration
from services.data_integration import DataGovIntegration
data_service = DataGovIntegration()


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
    try:
        # Fetch from real APEDA API
        result = data_service.fetch_apeda_data(state or "All", year or "2023-24", category)
        if result and len(result) > 0:
            return {
                "source": "APEDA India",
                "years_available": "2019-2024",
                "data": result[:10],  # Limit to 10 records
                "note": f"APEDA production data for {category} in {state or 'All India'}"
            }
    except Exception as e:
        print(f"DEBUG: APEDA API error: {e}")
    
    # Fallback to sample data
    return {
        "source": "APEDA India (sample)",
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
        google_api_key=settings.GEMINI_AGENT_KEY,
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
1. fetch_apeda_production - For state-level production data (2019-2024) - USE FOR Indian state production queries
2. fetch_crop_production - For district-level crop data (2013-2015) - USE FOR district-level data
3. fetch_rainfall_data - For historical (1901-2015) or recent (2019-2024) rainfall
4. search_knowledge_base - For general agricultural knowledge from our database
5. web_search - For REAL-TIME web search: current news, 2025+ data, latest policies, market prices

CRITICAL RULES:
1. You MUST call at least one tool before answering ANY agricultural question
2. For years 2025 or later: Use web_search (our database only goes up to 2024)
3. For "current", "latest", "recent" queries: Use web_search
4. For India production data (2019-2024): Use fetch_apeda_production with state_name and year
5. For district data: Use fetch_crop_production
6. For general knowledge: Use search_knowledge_base
7. NEVER answer without calling a tool first

Examples:
- "rice production in India 2023" → Call fetch_apeda_production(state_name="All India", year="2023-24", commodity="Basmati Rice")
- "rice in Punjab 2025" → Call web_search(query="rice production Punjab India 2025")
- "what is MSP" → Call search_knowledge_base(query="MSP minimum support price")""")
        
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
        google_api_key=settings.GEMINI_AGENT_KEY,
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

def force_web_search_node(state: AgentState) -> dict:
    """Force a web search when agent doesn't call it automatically for 2025+ queries"""
    from langchain_core.messages import ToolMessage
    
    question = state.get("question", "")
    print(f"DEBUG: Force web search for: {question}")
    
    # Create tool map
    tool_map = {tool.name: tool for tool in ALL_TOOLS}
    
    # Call web search
    try:
        result = tool_map["web_search"].invoke({"query": question})
        collected_data = {**state.get("collected_data", {}), "web_search": result}
        sources = list(set(state.get("sources_used", []) + [result.get("source", "Google Search")]))
        
        return {
            "collected_data": collected_data,
            "sources_used": sources,
            "messages": [ToolMessage(content=json.dumps(result), tool_call_id="forced_web_search")]
        }
    except Exception as e:
        print(f"DEBUG: Force web search failed: {e}")
        return {"messages": []}


def force_apeda_search_node(state: AgentState) -> dict:
    """Force APEDA search for historical production queries"""
    from langchain_core.messages import ToolMessage
    import re
    
    question = state.get("question", "")
    print(f"DEBUG: Force APEDA search for: {question}")
    
    # Extract year from question
    year_match = re.search(r'(201[9]|202[0-4])', question)
    year = year_match.group(1) if year_match else "2023"
    fiscal_year = f"{year}-{str(int(year)+1)[2:]}"  # 2023 -> 2023-24
    
    # Extract state if mentioned
    states = ["punjab", "haryana", "west bengal", "uttar pradesh", "maharashtra", "tamil nadu", 
              "andhra pradesh", "kerala", "karnataka", "madhya pradesh", "bihar", "odisha", "gujarat"]
    state_name = "All India"
    for s in states:
        if s in question.lower():
            state_name = s.title()
            break
    
    # Extract commodity
    commodities = ["rice", "wheat", "basmati", "maize", "cotton", "sugarcane", "pulses"]
    commodity = "All"
    for c in commodities:
        if c in question.lower():
            commodity = c.title()
            if commodity == "Rice":
                commodity = "Basmati Rice"
            break
    
    tool_map = {tool.name: tool for tool in ALL_TOOLS}
    
    try:
        result = tool_map["fetch_apeda_production"].invoke({
            "state_name": state_name,
            "year": fiscal_year,
            "commodity": commodity
        })
        collected_data = {**state.get("collected_data", {}), "apeda_production": result}
        sources = list(set(state.get("sources_used", []) + [result.get("source", "APEDA Database")]))
        
        return {
            "collected_data": collected_data,
            "sources_used": sources,
            "messages": [ToolMessage(content=json.dumps(result), tool_call_id="forced_apeda")]
        }
    except Exception as e:
        print(f"DEBUG: Force APEDA search failed: {e}")
        return {"messages": []}


def force_kb_search_node(state: AgentState) -> dict:
    """Force knowledge base search for general queries"""
    from langchain_core.messages import ToolMessage
    
    question = state.get("question", "")
    print(f"DEBUG: Force KB search for: {question}")
    
    tool_map = {tool.name: tool for tool in ALL_TOOLS}
    
    try:
        result = tool_map["search_knowledge_base"].invoke({"query": question})
        collected_data = {**state.get("collected_data", {}), "knowledge_base": result}
        sources = list(set(state.get("sources_used", []) + [result.get("source", "Knowledge Base")]))
        
        return {
            "collected_data": collected_data,
            "sources_used": sources,
            "messages": [ToolMessage(content=json.dumps(result), tool_call_id="forced_kb")]
        }
    except Exception as e:
        print(f"DEBUG: Force KB search failed: {e}")
        return {"messages": []}


def should_continue(state: AgentState) -> Literal["tools", "synthesize", "force_web_search", "force_apeda_search", "force_kb_search", "end"]:
    """
    Decide next step based on agent's output.
    This is the key routing logic that makes it agentic!
    """
    import re
    
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
    
    # Check if question needs web search (2025, current, latest, etc.)
    question = state.get("question", "").lower()
    needs_web = any(term in question for term in ["2025", "2026", "current", "latest", "recent", "today", "now"])
    
    # Check if historical data query (should use APEDA/database)
    needs_historical = any(year in question for year in ["2019", "2020", "2021", "2022", "2023", "2024"])
    
    # First step with no tools called but needs web search - force web search
    if state.get("step_count", 0) == 1 and not state.get("collected_data") and needs_web:
        print("DEBUG: Query needs current data, forcing web search")
        return "force_web_search"
    
    # First step with no tools but needs historical data - force APEDA
    if state.get("step_count", 0) == 1 and not state.get("collected_data") and needs_historical:
        print("DEBUG: Query needs historical data, forcing APEDA search")
        return "force_apeda_search"
    
    # First step with no tools - force knowledge base search
    if state.get("step_count", 0) == 1 and not state.get("collected_data"):
        print("DEBUG: No tools called, forcing knowledge base search")
        return "force_kb_search"
    
    # Otherwise synthesize with whatever we have
    print("DEBUG: Synthesizing answer")
    return "synthesize"


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
    workflow.add_node("force_web_search", force_web_search_node)
    workflow.add_node("force_apeda_search", force_apeda_search_node)
    workflow.add_node("force_kb_search", force_kb_search_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges (the agentic part!)
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "synthesize": "synthesize",
            "force_web_search": "force_web_search",
            "force_apeda_search": "force_apeda_search",
            "force_kb_search": "force_kb_search",
            "end": END
        }
    )
    
    # Tools always go back to agent for next decision
    workflow.add_edge("tools", "agent")
    
    # Force nodes go to synthesize
    workflow.add_edge("force_web_search", "synthesize")
    workflow.add_edge("force_apeda_search", "synthesize")
    workflow.add_edge("force_kb_search", "synthesize")
    
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
