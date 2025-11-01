"""
Test script to verify both models use different API keys
"""
import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

# Load environment variables
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

print("="*70)
print("TESTING TWO-MODEL ARCHITECTURE")
print("="*70)

# Get API keys
routing_key = os.environ.get('API_GUESSING_MODELKEY')
answer_key = os.environ.get('SECRET_KEY')

print(f"\n1. API Keys Configuration:")
print(f"   - Routing Key (API_GUESSING_MODELKEY): {routing_key[:20] if routing_key else 'NOT FOUND'}...")
print(f"   - Answer Key (SECRET_KEY): {answer_key[:20] if answer_key else 'NOT FOUND'}...")
print(f"   - Keys are different: {routing_key != answer_key}")

# Test QueryRouter
print(f"\n2. Testing QueryRouter (Model 1):")
print("   Initializing QueryRouter with routing key...")

try:
    import google.generativeai as genai
    
    # Initialize QueryRouter
    genai.configure(api_key=routing_key)
    router_model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Test simple prompt
    test_question = "What is rice production in Punjab for 2023-24?"
    print(f"   Question: {test_question}")
    
    simple_prompt = f"""Analyze this question and extract the year: {test_question}
    Return only the year in format: YYYY or YYYY-YY"""
    
    response = router_model.generate_content(simple_prompt)
    print(f"   ✅ QueryRouter Response: {response.text.strip()}")
    print(f"   ✅ QueryRouter is working with routing key!")
    
except Exception as e:
    print(f"   ❌ QueryRouter Error: {str(e)}")
    import traceback
    traceback.print_exc()

# Test QueryProcessor
print(f"\n3. Testing QueryProcessor (Model 2):")
print("   Initializing QueryProcessor with answer key...")

try:
    # Reconfigure with answer key
    genai.configure(api_key=answer_key)
    processor_model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Test simple prompt
    simple_prompt = "Answer in one sentence: What is agriculture?"
    
    response = processor_model.generate_content(simple_prompt)
    print(f"   ✅ QueryProcessor Response: {response.text.strip()[:100]}...")
    print(f"   ✅ QueryProcessor is working with answer key!")
    
except Exception as e:
    print(f"   ❌ QueryProcessor Error: {str(e)}")
    import traceback
    traceback.print_exc()

# Test routing logic
print(f"\n4. Testing Full Routing Logic:")
try:
    from app import QueryRouter
    
    router = QueryRouter(routing_key)
    test_questions = [
        "What is rice production in Punjab for 2023-24?",
        "Show wheat production in Karnataka for 2014",
        "What was rainfall in Pune in 2024?"
    ]
    
    for q in test_questions:
        print(f"\n   Question: {q}")
        params = router.route_query(q)
        print(f"   → data_needed: {params.get('data_needed', [])}")
        print(f"   → years: {params.get('years', [])}")
        print(f"   → states: {params.get('states', [])}")
        print(f"   → crops: {params.get('crops', [])}")
        
except Exception as e:
    print(f"   ❌ Routing Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)
