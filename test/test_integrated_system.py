"""
Test script to verify all integrated APIs in the main system
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_query(question, description):
    """Test a single query"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"Question: {question}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/query",
            json={"question": question},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"\nAnswer:\n{result.get('answer', 'No answer')}")
            
            # Show sources
            if 'sources' in result and result['sources']:
                print(f"\nData Sources Used:")
                for source in result['sources']:
                    print(f"  - {source}")
            
            # Show query results summary
            if 'query_results' in result:
                print(f"\nQuery Results Summary:")
                for key, value in result['query_results'].items():
                    if isinstance(value, dict) and 'data' in value:
                        data_count = len(value['data'])
                        print(f"  - {key}: {data_count} records")
            
            return True
        else:
            print(f"❌ Failed! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("INTEGRATED SYSTEM TESTING")
    print("Testing all APIs: Crop Production, APEDA, Daily Rainfall, Historical Rainfall")
    print("="*60)
    
    # Wait for server to be ready
    print("\nWaiting for server to be ready...")
    time.sleep(5)
    
    tests = [
        # Test 1: District-level crop data (2013-2015)
        (
            "What is the rice production in Punjab for 2014?",
            "District-level Crop Production API (2013-2015)"
        ),
        
        # Test 2: APEDA state-level data (2019-2024)
        (
            "What is the rice production in Punjab for 2023?",
            "APEDA Production API (2019-2024)"
        ),
        
        # Test 3: Daily rainfall (2019-2024)
        (
            "What was the rainfall in Pune in 2024?",
            "Daily Rainfall API (2019-2024)"
        ),
        
        # Test 4: Historical rainfall (1901-2015)
        (
            "Show me Punjab rainfall from 1950 to 1955",
            "Historical Rainfall API (1901-2015)"
        ),
        
        # Test 5: Comparison across time periods
        (
            "Compare Punjab rice production in 2014 and 2023",
            "Multi-source Query (Crop + APEDA)"
        ),
        
        # Test 6: APEDA with specific category
        (
            "What is the wheat production in Karnataka for 2022-23?",
            "APEDA with specific crop"
        ),
        
        # Test 7: Historical rainfall statistics
        (
            "What was the average annual rainfall in Punjab from 1980 to 1990?",
            "Historical Rainfall Statistics"
        ),
    ]
    
    results = []
    for question, description in tests:
        success = test_query(question, description)
        results.append((description, success))
        time.sleep(2)  # Small delay between requests
    
    # Summary
    print(f"\n\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    print("\nDetailed Results:")
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {description}")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
