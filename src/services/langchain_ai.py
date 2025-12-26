"""
LangChain-powered AI module with prompt templates and chains
Refactored from ai_models.py for better maintainability and extensibility
"""
import json
import os
from typing import Dict, List, Any, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import Tool
from pydantic import BaseModel, Field

from config.settings import settings


# ============================================================================
# PYDANTIC MODELS FOR STRUCTURED OUTPUT
# ============================================================================

class QueryRouteParams(BaseModel):
    """Structured parameters for query routing"""
    states: List[str] = Field(default_factory=list, description="Indian states mentioned")
    districts: List[str] = Field(default_factory=list, description="Districts mentioned")
    crops: List[str] = Field(default_factory=list, description="Crop names mentioned")
    crop_types: List[str] = Field(default_factory=list, description="Crop categories")
    years: List[str] = Field(default_factory=list, description="Years or year ranges")
    data_needed: List[str] = Field(default_factory=list, description="Data sources to query")
    comparison_type: Optional[str] = Field(default=None, description="Type of comparison")
    aggregation: Optional[str] = Field(default=None, description="Aggregation method")
    apeda_category: Optional[str] = Field(default=None, description="APEDA category")
    product_code: Optional[str] = Field(default=None, description="Product code if any")
    rainfall_type: Optional[str] = Field(default=None, description="daily or historical")


# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

QUERY_ROUTER_TEMPLATE = """You are an intelligent API router for agricultural data queries. 
Analyze this question and determine which data sources to use.

Question: {question}

Available Data Sources:
1. **crop_production** - District-level crop production (2013-2015)
   - Use for: District-specific crop data, detailed production by district
   - Years: 2013, 2014, 2015

2. **apeda_production** - State-level aggregated production (2019-2024)
   - Use for: Recent state-level crop/livestock/fruits/vegetables data
   - Years: 2019, 2020, 2021, 2022, 2023, 2024
   - Categories: Agri (grains/cereals), Fruits, Vegetables, Spices, LiveStock, Plantations, Floriculture

3. **daily_rainfall** - District-wise daily rainfall (2019-2024)
   - Use for: Recent rainfall data, district-specific rainfall
   - Years: 2019-2024

4. **historical_rainfall** - State-wise historical rainfall (1901-2015)
   - Use for: Long-term rainfall trends, historical analysis
   - Years: 1901-2015

5. **rainfall** - Sample rainfall data (fallback)
   - Use only if no specific year mentioned and other rainfall sources don't apply

ROUTING RULES:
- For PRODUCTION queries:
  * Years 2019-2024 → use "apeda_production"
  * Years 2013-2015 → use "crop_production"
  * No year specified → use BOTH ["crop_production", "apeda_production"]

- For RAINFALL queries:
  * Years 2019-2024 → use "daily_rainfall"
  * Years 1901-2015 → use "historical_rainfall"
  * No year specified → use "rainfall" (sample data)

- For COMPARISON queries:
  * Select multiple sources if comparing different time periods

Return ONLY valid JSON in this exact format:
{{
  "states": ["State1", "State2"],
  "districts": ["District1"],
  "crops": ["rice", "wheat"],
  "crop_types": ["cereals"],
  "years": ["2023-24"] or ["2023"] or ["1950", "1951"],
  "data_needed": ["apeda_production"] or ["crop_production", "apeda_production"],
  "comparison_type": "temporal" | "spatial" | "correlation" | null,
  "aggregation": "sum" | "average" | "top" | "trend" | null,
  "apeda_category": "Agri" | "Fruits" | "Vegetables" | "Spices" | "LiveStock" | null,
  "product_code": null,
  "rainfall_type": "daily" | "historical" | null
}}

Return ONLY the JSON, no other text."""


ANSWER_GENERATION_TEMPLATE = """You are an expert agricultural data analyst with access to multiple comprehensive datasets.
Answer this question using the provided data.

Question: {question}

Available Data:
{query_results}

Data Sources Used:
{data_sources}

IMPORTANT Instructions:
1. Answer the question accurately and completely
2. Include specific numbers and statistics from the data
3. For EVERY data point mentioned, cite the source using this format: [Source: dataset_name]
4. If the data includes "years_used", "note", or "metadata" fields, EXPLICITLY mention which years the data covers
5. If NO DATA is found (empty data array), check the "metadata" field for "available_years" and tell the user what years ARE available
6. If comparing multiple entities, present in a clear structured format
7. If showing trends, describe the pattern clearly
8. Be transparent about the time period covered by the data
9. Keep the answer concise but comprehensive
10. You have access to multiple datasets:
    - District-wise Crop Production (2013-2014): District-level crop data
    - APEDA Production (2019-2024): State-level aggregated production for recent years
    - Daily Rainfall (2019-2024): District-wise daily rainfall
    - Historical Rainfall (1901-2015): State-wise historical rainfall with monthly/seasonal/annual data
    - Choose and mention the most relevant dataset(s) for the query

Provide your answer:"""


# ============================================================================
# LANGCHAIN QUERY ROUTER
# ============================================================================

class LangChainQueryRouter:
    """
    LangChain-powered query router using prompt templates and chains
    Uses LCEL (LangChain Expression Language) for clean pipeline composition
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GEMINI_ROUTING_KEY
        print(f"DEBUG: Initializing LangChainQueryRouter...")
        
        if not self.api_key:
            raise ValueError("LangChainQueryRouter requires an API key")
        
        # Initialize Gemini via LangChain
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.1,  # Low temperature for consistent routing
            convert_system_message_to_human=True
        )
        
        # Create prompt template
        self.prompt = PromptTemplate(
            template=QUERY_ROUTER_TEMPLATE,
            input_variables=["question"]
        )
        
        # Create output parser
        self.output_parser = JsonOutputParser(pydantic_object=QueryRouteParams)
        
        # Build the chain using LCEL
        self.chain = self.prompt | self.llm | StrOutputParser()
        
        print("DEBUG: LangChainQueryRouter initialized successfully!")
    
    def route_query(self, question: str) -> Dict[str, Any]:
        """
        Route query using LangChain chain
        Returns structured parameters for query execution
        """
        try:
            print("DEBUG: LangChainQueryRouter analyzing question...")
            
            # Invoke the chain
            response = self.chain.invoke({"question": question})
            print(f"DEBUG: LangChainQueryRouter response: {len(response)} chars")
            
            # Parse JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                params = json.loads(json_str)
                print(f"DEBUG: LangChainQueryRouter extracted params: {params}")
                return params
            
        except Exception as e:
            print(f"DEBUG: LangChainQueryRouter error: {str(e)}")
        
        # Fallback parameters
        print("DEBUG: LangChainQueryRouter using fallback parameters")
        return self._get_fallback_params()
    
    def _get_fallback_params(self) -> Dict[str, Any]:
        """Return default fallback parameters"""
        return {
            "states": [],
            "districts": [],
            "crops": [],
            "crop_types": [],
            "years": [],
            "data_needed": ["crop_production", "rainfall"],
            "comparison_type": None,
            "aggregation": None,
            "apeda_category": None,
            "product_code": None,
            "rainfall_type": None
        }


# ============================================================================
# LANGCHAIN QUERY PROCESSOR
# ============================================================================

class LangChainQueryProcessor:
    """
    LangChain-powered query processor for generating answers
    Uses prompt templates for maintainable answer generation
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        print(f"DEBUG: Initializing LangChainQueryProcessor...")
        
        if not self.api_key:
            raise ValueError("LangChainQueryProcessor requires an API key")
        
        # Initialize Gemini via LangChain
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.7,  # Higher temperature for natural responses
            convert_system_message_to_human=True
        )
        
        # Create prompt template
        self.prompt = PromptTemplate(
            template=ANSWER_GENERATION_TEMPLATE,
            input_variables=["question", "query_results", "data_sources"]
        )
        
        # Build the chain
        self.chain = self.prompt | self.llm | StrOutputParser()
        
        print("DEBUG: LangChainQueryProcessor initialized successfully!")
    
    def generate_answer(
        self, 
        question: str, 
        query_results: Dict[str, Any], 
        data_sources: List[str]
    ) -> str:
        """Generate natural language answer using LangChain chain"""
        try:
            print("DEBUG: LangChainQueryProcessor generating answer...")
            
            # Invoke the chain with context
            answer = self.chain.invoke({
                "question": question,
                "query_results": json.dumps(query_results, indent=2),
                "data_sources": json.dumps(data_sources, indent=2)
            })
            
            print(f"DEBUG: Answer generated: {len(answer)} characters")
            return answer
            
        except Exception as e:
            print(f"DEBUG: LangChainQueryProcessor error: {str(e)}")
            import traceback
            traceback.print_exc()
            return "Error generating answer. Please try again."


# ============================================================================
# LANGCHAIN TOOLS (For Agentic Workflows)
# ============================================================================

def create_data_tools(data_fetchers: Dict) -> List[Tool]:
    """
    Create LangChain Tools from data fetcher functions
    This enables agentic behavior where the LLM decides which tools to call
    """
    tools = []
    
    # Tool definitions with descriptions
    tool_definitions = [
        {
            "name": "fetch_apeda_data",
            "description": "Fetch state-level agricultural production data (2019-2024). "
                          "Categories: Agri, Fruits, Vegetables, Spices, LiveStock, Floriculture. "
                          "Use for recent production statistics.",
            "func_key": "apeda"
        },
        {
            "name": "fetch_crop_production",
            "description": "Fetch district-level crop production data (2013-2015). "
                          "Use for detailed district-wise crop statistics.",
            "func_key": "crop"
        },
        {
            "name": "fetch_daily_rainfall",
            "description": "Fetch district-wise daily rainfall data (2019-2024). "
                          "Use for recent rainfall patterns and analysis.",
            "func_key": "daily_rainfall"
        },
        {
            "name": "fetch_historical_rainfall",
            "description": "Fetch state-wise historical rainfall data (1901-2015). "
                          "Use for long-term rainfall trends and climate analysis.",
            "func_key": "historical_rainfall"
        }
    ]
    
    for tool_def in tool_definitions:
        if tool_def["func_key"] in data_fetchers:
            tool = Tool(
                name=tool_def["name"],
                description=tool_def["description"],
                func=data_fetchers[tool_def["func_key"]]
            )
            tools.append(tool)
    
    return tools


# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================

# Alias for backward compatibility with existing code
QueryRouter = LangChainQueryRouter
QueryProcessor = LangChainQueryProcessor


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def get_query_router(use_langchain: bool = True) -> LangChainQueryRouter:
    """Factory function to get query router instance"""
    if use_langchain:
        return LangChainQueryRouter()
    else:
        # Fallback to legacy implementation if needed
        from services.ai_models import QueryRouter as LegacyRouter
        return LegacyRouter(settings.GEMINI_ROUTING_KEY)


def get_query_processor(use_langchain: bool = True) -> LangChainQueryProcessor:
    """Factory function to get query processor instance"""
    if use_langchain:
        return LangChainQueryProcessor()
    else:
        # Fallback to legacy implementation if needed
        from services.ai_models import QueryProcessor as LegacyProcessor
        return LegacyProcessor(settings.GEMINI_API_KEY)
