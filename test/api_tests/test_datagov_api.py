"""
Test script to fetch real data from data.gov.in API
Based on the API documentation from: https://data.gov.in/resource/district-wise-season-wise-crop-production-statistics-1997
"""

import requests
import json
from typing import Dict, List, Any


class DataGovAPITester:
    """Test class for data.gov.in API"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize API tester
        
        Args:
            api_key: Your data.gov.in API key. Get one from: https://data.gov.in/
                    Default sample key provided (limited to 10 records)
        """
        # Sample API key from data.gov.in documentation
        self.api_key = api_key or "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
        self.base_url = "https://api.data.gov.in/resource"
        
    def test_crop_production_api(self, limit: int = 10, offset: int = 0, format: str = "json") -> Dict[str, Any]:
        """
        Test the District-wise Crop Production Statistics API
        
        Args:
            limit: Maximum number of records to return (default 10)
            offset: Number of records to skip (for pagination)
            format: Response format (json, xml, csv)
            
        Returns:
            API response as dictionary
        """
        # API endpoint for crop production statistics
        resource_id = "35be999b-0208-4354-b557-f6ca9a5355de"
        
        url = f"{self.base_url}/{resource_id}"
        
        params = {
            'api-key': self.api_key,
            'format': format,
            'limit': limit,
            'offset': offset
        }
        
        print(f"\n{'='*70}")
        print(f"🌾 TESTING CROP PRODUCTION API")
        print(f"{'='*70}")
        print(f"URL: {url}")
        print(f"Parameters: {json.dumps(params, indent=2)}")
        print(f"{'='*70}\n")
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            print(f"✅ Status Code: {response.status_code}")
            print(f"✅ Response Headers:")
            for key, value in response.headers.items():
                print(f"   {key}: {value}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✅ SUCCESS! Received data:")
                print(f"   Total fields: {len(data.get('fields', []))}")
                print(f"   Total records: {len(data.get('records', []))}")
                
                if data.get('fields'):
                    print(f"\n📋 Available Fields:")
                    for field in data['fields']:
                        print(f"   - {field['name']} ({field['type']})")
                
                if data.get('records'):
                    print(f"\n📊 Sample Records (showing first 3):")
                    for i, record in enumerate(data['records'][:3], 1):
                        print(f"\n   Record {i}:")
                        for key, value in record.items():
                            print(f"      {key}: {value}")
                
                return data
            else:
                print(f"\n❌ ERROR: Status code {response.status_code}")
                print(f"Response: {response.text}")
                return {'error': response.text}
                
        except requests.exceptions.Timeout:
            print(f"\n❌ ERROR: Request timed out after 30 seconds")
            return {'error': 'Timeout'}
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': str(e)}
    
    def test_with_filters(self, state: str = "Punjab", crop: str = "Rice", limit: int = 10):
        """
        Test API with specific filters
        
        Args:
            state: State name to filter by
            crop: Crop name to filter by
            limit: Max records to return
        """
        resource_id = "35be999b-0208-4354-b557-f6ca9a5355de"
        url = f"{self.base_url}/{resource_id}"
        
        params = {
            'api-key': self.api_key,
            'format': 'json',
            'limit': limit,
            'filters[state_name]': state,
            'filters[crop]': crop
        }
        
        print(f"\n{'='*70}")
        print(f"🔍 TESTING API WITH FILTERS")
        print(f"{'='*70}")
        print(f"State: {state}")
        print(f"Crop: {crop}")
        print(f"Limit: {limit}")
        print(f"{'='*70}\n")
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS! Filtered results:")
                print(f"   Records found: {len(data.get('records', []))}")
                
                if data.get('records'):
                    print(f"\n📊 Filtered Data:")
                    for i, record in enumerate(data['records'][:5], 1):
                        print(f"\n   {i}. {record.get('district_name', 'N/A')} - {record.get('crop_year', 'N/A')}")
                        print(f"      Production: {record.get('production', 'N/A')} tonnes")
                        print(f"      Area: {record.get('area', 'N/A')} hectares")
                
                return data
            else:
                print(f"❌ ERROR: Status code {response.status_code}")
                print(f"Response: {response.text}")
                return {'error': response.text}
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            return {'error': str(e)}
    
    def save_to_file(self, data: Dict[str, Any], filename: str = "api_response.json"):
        """Save API response to JSON file"""
        try:
            filepath = f"C:\\Users\\Lenovo\\Desktop\\Project samarth\\test\\api_tests\\{filename}"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Data saved to: {filepath}")
        except Exception as e:
            print(f"\n❌ Error saving file: {str(e)}")


def run_all_tests():
    """Run all API tests"""
    print(f"\n{'#'*70}")
    print(f"# DATA.GOV.IN API TESTING SUITE")
    print(f"# Project Samarth - Agricultural Data Integration")
    print(f"{'#'*70}")
    
    # Initialize tester with sample API key
    tester = DataGovAPITester()
    
    # Test 1: Basic API call
    print(f"\n\n{'='*70}")
    print(f"TEST 1: Basic API Call (10 records)")
    print(f"{'='*70}")
    data = tester.test_crop_production_api(limit=10)
    if data and not data.get('error'):
        tester.save_to_file(data, "basic_test.json")
    
    # Test 2: Larger dataset
    print(f"\n\n{'='*70}")
    print(f"TEST 2: Fetch 50 records")
    print(f"{'='*70}")
    data = tester.test_crop_production_api(limit=50)
    if data and not data.get('error'):
        tester.save_to_file(data, "large_test.json")
    
    # Test 3: Filtered query - Punjab Rice
    print(f"\n\n{'='*70}")
    print(f"TEST 3: Filtered Query - Punjab Rice")
    print(f"{'='*70}")
    data = tester.test_with_filters(state="Punjab", crop="Rice", limit=20)
    if data and not data.get('error'):
        tester.save_to_file(data, "punjab_rice.json")
    
    # Test 4: Karnataka Groundnut
    print(f"\n\n{'='*70}")
    print(f"TEST 4: Filtered Query - Karnataka Groundnut")
    print(f"{'='*70}")
    data = tester.test_with_filters(state="Karnataka", crop="Groundnut", limit=20)
    if data and not data.get('error'):
        tester.save_to_file(data, "karnataka_groundnut.json")
    
    print(f"\n\n{'#'*70}")
    print(f"# ALL TESTS COMPLETED")
    print(f"{'#'*70}")
    print(f"\n📝 NOTES:")
    print(f"   - Sample API key has a limit of 10 records per request")
    print(f"   - To get your own API key, visit: https://data.gov.in/")
    print(f"   - Login to data.gov.in -> Go to 'My Account' section")
    print(f"   - Your API key will be displayed there")
    print(f"   - Results saved in: test/api_tests/ folder")
    print(f"\n")


if __name__ == "__main__":
    run_all_tests()
