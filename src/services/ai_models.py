"""AI models for query routing and processing"""
import json
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")
import google.generativeai as genai


class QueryRouter:
    """
    Specialized Gemini model for routing queries to correct APIs
    Uses a separate API key for intelligent query routing
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        print(f"DEBUG: Initializing QueryRouter with API key: {api_key[:20] if api_key else 'None'}...")
        
        if not self.api_key:
            raise ValueError("QueryRouter requires an API key")
        
        try:
            # Configure Gemini with routing key
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')  # Fast model for routing
            print("DEBUG: QueryRouter Gemini model initialized successfully!")
        except Exception as e:
            print(f"DEBUG: Error initializing QueryRouter: {str(e)}")
            raise
    
    def route_query(self, question: str) -> dict:
        """
        Determine which APIs to call based on the question
        Returns structured parameters for query execution
        """
        
        prompt = f"""You are an intelligent API router for agricultural data queries. Analyze this question and determine which data sources to use.

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

        try:
            print("DEBUG: QueryRouter analyzing question...")
            response = self.model.generate_content(prompt)
            response_text = response.text
            print(f"DEBUG: QueryRouter response received: {len(response_text)} chars")
            
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                params = json.loads(json_str)
                print(f"DEBUG: QueryRouter extracted params: {params}")
                return params
            else:
                print(f"DEBUG: QueryRouter could not find JSON in response")
        except Exception as e:
            print(f"DEBUG: QueryRouter error: {str(e)}")
        
        # Fallback: default parameters
        print("DEBUG: QueryRouter using fallback parameters")
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


class QueryProcessor:
    """Processes natural language queries using Gemini API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        print(f"DEBUG: Initializing QueryProcessor with API key: {api_key[:20] if api_key else 'None'}...")
        
        if not self.api_key:
            raise ValueError("QueryProcessor requires an API key")
        
        try:
            # Configure Gemini with answer generation key
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            print("DEBUG: QueryProcessor Gemini model initialized successfully!")
        except Exception as e:
            print(f"DEBUG: Error initializing QueryProcessor: {str(e)}")
            raise
    
    def generate_answer(self, question: str, query_results: dict, data_sources: list) -> str:
        """Generate natural language answer with citations"""
        
        prompt = f"""You are an expert agricultural data analyst with access to multiple comprehensive datasets. Answer this question using the provided data.

Question: {question}

Available Data:
{json.dumps(query_results, indent=2)}

Data Sources Used:
{json.dumps(data_sources, indent=2)}

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

        try:
            print("DEBUG: Generating answer with Gemini...")
            response = self.model.generate_content(prompt)
            print(f"DEBUG: Answer generated: {len(response.text) if response.text else 0} characters")
            return response.text
        except Exception as e:
            print(f"DEBUG: Gemini API Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return "Error generating answer. Please try again."
