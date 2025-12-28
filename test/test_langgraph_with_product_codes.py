"""Test the complete LangGraph agent with product code matching"""
import sys
sys.path.append('c:/Users/Lenovo/Desktop/Project samarth/src')

import asyncio
from services.langgraph_agent import process_query_with_langgraph

async def main():
    test_queries = [
        "What is the rice production in Punjab for 2023-24?",
        "Tell me wheat production in Haryana for 2023",
        "What is mango production in Maharashtra 2024?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print("\n" + "=" * 80)
        print(f"TEST {i}: {query}")
        print("=" * 80)
        
        try:
            result = await process_query_with_langgraph(query)
            print(f"\n✓ Result: {result['answer'][:500]}")
            print(f"\n  Sources used: {result.get('sources', 'None')}")
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
