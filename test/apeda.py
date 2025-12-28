"""
Direct APEDA API Test
Test the APEDA API to see what data it actually returns
"""
import requests
import json

APEDA_URL = "https://agriexchange.apeda.gov.in/Production/IndiaCat/GetIndiaProductionCatObject"

def test_apeda_api(fin_year, category="All", product_code="All", report_type="1"):
    """Test APEDA API with different parameters"""
    
    payload = {
        "Category": category,
        "Financial_Year": fin_year,
        "product_code": product_code,
        "ReportType": report_type
    }
    
    print("\n" + "="*80)
    print(f"Testing APEDA API")
    print("="*80)
    print(f"URL: {APEDA_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("="*80)
    
    try:
        response = requests.post(
            APEDA_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=30
        )
        
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Response Data Type: {type(data)}")
            
            if isinstance(data, list):
                print(f"📊 Number of Records: {len(data)}")
                
                if len(data) > 0:
                    print(f"\n📋 Sample Record (First Item):")
                    print(json.dumps(data[0], indent=2))
                    
                    if len(data) > 1:
                        print(f"\n📋 Sample Record (Second Item):")
                        print(json.dumps(data[1], indent=2))
                    
                    # Print all column names
                    print(f"\n🔑 Available Columns:")
                    for key in data[0].keys():
                        print(f"  - {key}")
                    
                    # Print all records in a compact format
                    print(f"\n📊 All Records:")
                    for i, record in enumerate(data[:20]):  # Show first 20 records
                        print(f"\nRecord {i+1}:")
                        print(json.dumps(record, indent=2))
                    
                    if len(data) > 20:
                        print(f"\n... and {len(data) - 20} more records")
                else:
                    print("\n⚠️ No records returned (empty list)")
            
            elif isinstance(data, dict):
                print(f"\n📊 Response is a dictionary:")
                print(json.dumps(data, indent=2))
            
            else:
                print(f"\n⚠️ Unexpected data type: {type(data)}")
                print(f"Raw data: {data}")
        
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response Text: {response.text}")
    
    except Exception as e:
        print(f"\n❌ Exception occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n🧪 APEDA API Testing Suite - RICE PRODUCT CODE")
    print("="*80)
    
    # Test 1: Rice - Product code 1011
    print("\n\n🧪 TEST 1: RICE product_code=1011, 2023-24")
    test_apeda_api(fin_year="2023-24", category="Agri", product_code="1011")
    
    # Test 2: Rice 2022-23
    print("\n\n🧪 TEST 2: RICE product_code=1011, 2022-23")
    test_apeda_api(fin_year="2022-23", category="Agri", product_code="1011")
    
    # Test 3: Rice with Category=All
    print("\n\n🧪 TEST 3: RICE product_code=1011, Category=All")
    test_apeda_api(fin_year="2023-24", category="All", product_code="1011")
    
    print("\n\n" + "="*80)
    print("✅ Testing Complete!")
    print("="*80)
