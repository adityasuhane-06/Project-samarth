"""
Test script for LangChain + RAG integration
Run this to verify the setup before your Techolution interview!
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()


def test_langchain_router():
    """Test the LangChain Query Router"""
    print("\n" + "="*60)
    print("TEST 1: LangChain Query Router")
    print("="*60)
    
    try:
        from services.langchain_ai import LangChainQueryRouter
        
        router = LangChainQueryRouter()
        
        # Test queries
        test_queries = [
            "What is rice production in Punjab in 2023?",
            "Show me rainfall trends in Maharashtra from 1950 to 1960",
            "Compare wheat production across states"
        ]
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            result = router.route_query(query)
            print(f"Routed to: {result.get('data_needed', [])}")
            print(f"Years: {result.get('years', [])}")
        
        print("\n✅ LangChain Query Router: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ LangChain Query Router: FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_langchain_processor():
    """Test the LangChain Query Processor"""
    print("\n" + "="*60)
    print("TEST 2: LangChain Query Processor")
    print("="*60)
    
    try:
        from services.langchain_ai import LangChainQueryProcessor
        
        processor = LangChainQueryProcessor()
        
        # Test with mock data
        mock_data = {
            "crop_production": {
                "data": [
                    {"state": "Punjab", "crop": "Rice", "production": 12000000, "year": 2023}
                ]
            }
        }
        
        answer = processor.generate_answer(
            question="What is rice production in Punjab?",
            query_results=mock_data,
            data_sources=["crop_production"]
        )
        
        print(f"\nGenerated Answer (first 200 chars):")
        print(answer[:200] + "..." if len(answer) > 200 else answer)
        
        print("\n✅ LangChain Query Processor: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ LangChain Query Processor: FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rag_service():
    """Test the RAG Service with ChromaDB"""
    print("\n" + "="*60)
    print("TEST 3: RAG Service (ChromaDB)")
    print("="*60)
    
    try:
        from services.rag_service import get_rag_service
        
        # Use local storage for testing (free, no cloud needed)
        rag = get_rag_service(use_cloud=False)
        
        # Get stats
        stats = rag.get_collection_stats()
        print(f"\nCollection Stats: {stats}")
        
        # Test search
        print("\nSearching for 'rice production Punjab'...")
        results = rag.search("rice production Punjab", k=2)
        
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"  Content: {doc['content'][:100]}...")
            print(f"  Source: {doc['metadata'].get('source', 'unknown')}")
        
        # Test RAG answer
        print("\nTesting RAG-powered answer...")
        answer = rag.query_with_rag("What data sources are available for rainfall?")
        print(f"Answer: {answer[:300]}...")
        
        print("\n✅ RAG Service: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ RAG Service: FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_backward_compatibility():
    """Test that existing code still works"""
    print("\n" + "="*60)
    print("TEST 4: Backward Compatibility")
    print("="*60)
    
    try:
        # Old imports should still work
        from services.ai_models import QueryRouter, QueryProcessor
        
        router = QueryRouter(os.getenv('API_GUESSING_MODELKEY'))
        processor = QueryProcessor(os.getenv('SECRET_KEY'))
        
        # Quick test
        result = router.route_query("test query")
        assert "data_needed" in result
        
        print("\n✅ Backward Compatibility: PASSED")
        print("  (Original ai_models.py still works)")
        return True
        
    except Exception as e:
        print(f"\n❌ Backward Compatibility: FAILED")
        print(f"Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "🚀"*30)
    print("\n  PROJECT SAMARTH - LANGCHAIN + RAG TEST SUITE")
    print("  For Techolution Gen AI/ML Interview")
    print("\n" + "🚀"*30)
    
    results = []
    
    # Run tests
    results.append(("LangChain Router", test_langchain_router()))
    results.append(("LangChain Processor", test_langchain_processor()))
    results.append(("RAG Service", test_rag_service()))
    results.append(("Backward Compatibility", test_backward_compatibility()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED! You're ready for the interview!")
        print("\nKey talking points:")
        print("  1. LangChain LCEL (LangChain Expression Language) for clean pipelines")
        print("  2. Prompt Templates for maintainable prompts")
        print("  3. ChromaDB for vector storage in RAG")
        print("  4. Google Generative AI Embeddings for semantic search")
        print("  5. Two-model architecture refactored with LangChain")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
    
    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
