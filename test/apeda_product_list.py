"""
Try to find the APEDA product list - deep investigation
"""
import requests
import re
import json

APEDA_BASE = "https://agriexchange.apeda.gov.in"

def fetch_page_and_analyze():
    """Fetch the main page and analyze all JavaScript references"""
    url = f"{APEDA_BASE}/Production/IndiaCat"
    print(f"Fetching: {url}")
    
    response = requests.get(url, timeout=15)
    html = response.text
    
    # Look for any JavaScript files
    js_files = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html)
    print(f"\nFound {len(js_files)} JavaScript files:")
    for js_file in js_files:
        print(f"  - {js_file}")
    
    # Look for inline JavaScript that might contain API endpoints
    print("\n\nSearching for API endpoints in page source...")
    
    # Common patterns for API calls
    patterns = [
        r'fetch\(["\']([^"\']+)["\']',
        r'\$\.ajax\(["\']?url["\']?\s*:\s*["\']([^"\']+)["\']',
        r'\$\.get\(["\']([^"\']+)["\']',
        r'\$\.post\(["\']([^"\']+)["\']',
        r'axios\.[a-z]+\(["\']([^"\']+)["\']',
        r'url\s*:\s*["\']([^"\']+)["\']',
    ]
    
    found_urls = set()
    for pattern in patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        found_urls.update(matches)
    
    print(f"Found {len(found_urls)} potential API URLs:")
    for url in sorted(found_urls):
        if 'product' in url.lower() or 'category' in url.lower() or 'dropdown' in url.lower():
            print(f"  *** {url}")
        else:
            print(f"      {url}")
    
    # Look for data embedded in the HTML
    print("\n\nSearching for embedded data...")
    
    # Look for JSON data
    json_patterns = [
        r'var\s+products\s*=\s*(\[.*?\]);',
        r'let\s+products\s*=\s*(\[.*?\]);',
        r'const\s+products\s*=\s*(\[.*?\]);',
        r'productList\s*=\s*(\[.*?\]);',
        r'productData\s*=\s*(\[.*?\]);',
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, html, re.DOTALL)
        if matches:
            print(f"\nFound product data with pattern: {pattern}")
            for match in matches:
                try:
                    data = json.loads(match)
                    print(f"  Successfully parsed {len(data)} products!")
                    print(f"  Sample: {data[:3]}")
                    return data
                except:
                    print(f"  Found data but couldn't parse as JSON")
    
    return None

def try_common_mvc_endpoints():
    """Try common ASP.NET MVC/Web API endpoint patterns"""
    print("\n\nTrying common MVC/Web API patterns...")
    
    endpoints = [
        # ASP.NET MVC patterns
        "/Production/GetProducts",
        "/Production/GetProductsByCategory",
        "/Production/ProductList",
        "/api/Production/Products",
        "/api/Products",
        "/api/Products/GetByCategory?category=Agri",
        
        # With different HTTP methods and parameters
        ("/Production/IndiaCat/GetProducts", "POST", {"Category": "Agri"}),
        ("/Production/IndiaCat/Products", "POST", {"Category": "Agri"}),
        ("/api/GetProducts", "GET", None),
    ]
    
    for item in endpoints:
        if isinstance(item, tuple):
            endpoint, method, data = item
        else:
            endpoint, method, data = item, "GET", None
        
        url = f"{APEDA_BASE}{endpoint}"
        print(f"\n{method} {url}")
        
        try:
            if method == "POST":
                if data:
                    response = requests.post(url, json=data, timeout=10)
                else:
                    response = requests.post(url, timeout=10)
            else:
                response = requests.get(url, timeout=10)
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  SUCCESS! Content-Type: {response.headers.get('Content-Type')}")
                print(f"  Response length: {len(response.text)}")
                
                # Try to parse as JSON
                try:
                    json_data = response.json()
                    print(f"  JSON response with {len(json_data) if isinstance(json_data, list) else '?'} items")
                    print(f"  Sample: {json_data[:3] if isinstance(json_data, list) else json_data}")
                    return json_data
                except:
                    print(f"  Not JSON, first 500 chars: {response.text[:500]}")
        
        except Exception as e:
            print(f"  Error: {str(e)[:100]}")
    
    return None

if __name__ == "__main__":
    print("="*80)
    print("APEDA Product List - Testing discovered endpoints!")
    print("="*80)
    
    # Test the discovered endpoints
    endpoints = [
        "/Production/IndiaCat/GetIndiaProductionCat",
        "/Production/IndiaCat/GetIndiaProductionCatYears",
        "/Production/IndiaCat/GetIndiaProductionCatProduct",
    ]
    
    for endpoint in endpoints:
        url = f"{APEDA_BASE}{endpoint}"
        print(f"\n{'='*80}")
        print(f"Testing: {endpoint}")
        print(f"{'='*80}")
        
        # Try GET
        print("\nGET request:")
        try:
            response = requests.get(url, timeout=10)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  SUCCESS! JSON response")
                    print(f"  Type: {type(data)}")
                    if isinstance(data, list):
                        print(f"  Items: {len(data)}")
                        print(f"  Sample (first 10):")
                        for item in data[:10]:
                            print(f"    {item}")
                    else:
                        print(f"  Data: {data}")
                except:
                    print(f"  Response (first 500 chars): {response.text[:500]}")
        except Exception as e:
            print(f"  Error: {e}")
        
        # Try POST with empty body
        print("\nPOST request (empty):")
        try:
            response = requests.post(url, json={}, timeout=10)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  SUCCESS! JSON response")
                    print(f"  Type: {type(data)}")
                    if isinstance(data, list):
                        print(f"  Items: {len(data)}")
                        print(f"  Sample (first 10):")
                        for item in data[:10]:
                            print(f"    {item}")
                    else:
                        print(f"  Data: {data}")
                except:
                    print(f"  Response (first 500 chars): {response.text[:500]}")
        except Exception as e:
            print(f"  Error: {e}")
        
        # Try POST with Category parameter
        print("\nPOST request (with Category=Agri):")
        try:
            response = requests.post(url, json={"Category": "Agri"}, timeout=10)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  SUCCESS! JSON response")
                    print(f"  Type: {type(data)}")
                    if isinstance(data, list):
                        print(f"  Items: {len(data)}")
                        print(f"  Sample (first 15):")
                        for item in data[:15]:
                            print(f"    {item}")
                    else:
                        print(f"  Data: {data}")
                except:
                    print(f"  Response (first 500 chars): {response.text[:500]}")
        except Exception as e:
            print(f"  Error: {e}")

