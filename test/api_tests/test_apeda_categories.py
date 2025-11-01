"""
Test APEDA API with correct categories from the website form
Based on the HTML form structure from agriexchange.apeda.gov.in
"""

import requests
import pandas as pd
import json
from datetime import datetime
import time

APEDA_URL = "https://agriexchange.apeda.gov.in/Production/IndiaCat/GetIndiaProductionCatObject"

def fetch_apeda_data(fin_year: str, category: str = "All", product_code: str = "All", report_type: str = "1"):
    """
    Fetch data from APEDA API with correct parameters
    
    Categories from form:
    - All
    - Floriculture
    - Agri
    - LiveStock
    - Fruits
    - Vegetables
    - Spices
    - Plantations
    
    Product codes are numeric (e.g., "1011" for Rice, "1013" for Wheat)
    Report Type: "1" = Summary, "2" = Detailed
    """
    payload = {
        "Category": category,
        "Financial_Year": fin_year,
        "product_code": product_code,
        "ReportType": report_type
    }
    
    print(f"\nFetching: {fin_year} | Category: {category} | Product: {product_code} | Type: {report_type}")
    
    try:
        r = requests.post(APEDA_URL, json=payload, headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }, timeout=30)
        
        r.raise_for_status()
        data = r.json()
        
        # Check if response is a list (successful)
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            
            # Normalize column names
            rename_map = {}
            for col in df.columns:
                col_lower = col.lower().strip()
                if col_lower.startswith("state"):
                    rename_map[col] = "State"
                elif "production" in col_lower:
                    rename_map[col] = "Production"
                elif "percent" in col_lower:
                    rename_map[col] = "Percent_Share"
            
            if rename_map:
                df = df.rename(columns=rename_map)
            
            # Add metadata
            df["Financial_Year"] = fin_year
            df["Category"] = category
            df["Product_Code"] = product_code
            
            # Convert production to numeric
            if "Production" in df.columns:
                df["Production"] = pd.to_numeric(df["Production"], errors="coerce")
            
            print(f"✓ Success: {len(df)} rows, {len(df.columns)} columns")
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"apeda_{category}_{product_code}_{fin_year}_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return df
        else:
            print(f"✗ Failed: Response type = {type(data)}, Value = {data}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return pd.DataFrame()


def test_categories():
    """Test different categories"""
    
    print("\n" + "="*80)
    print("TESTING DIFFERENT CATEGORIES WITH CORRECT PARAMETERS")
    print("="*80)
    
    # Categories from the HTML form
    categories = ["All", "Agri", "Fruits", "Vegetables", "Spices", "LiveStock", "Plantations", "Floriculture"]
    
    fin_year = "2023-24"
    results = []
    
    for category in categories:
        print(f"\n{'='*80}")
        print(f"CATEGORY: {category}")
        print(f"{'='*80}")
        
        df = fetch_apeda_data(fin_year=fin_year, category=category, product_code="All", report_type="1")
        
        success = len(df) > 0
        results.append({
            "Category": category,
            "Year": fin_year,
            "Success": "✓" if success else "✗",
            "Rows": len(df),
            "Columns": len(df.columns) if success else 0
        })
        
        if success:
            print(f"\nTop 5 States by Production:")
            if "Production" in df.columns and "State" in df.columns:
                top_states = df.nlargest(5, "Production")[["State", "Production"]]
                for idx, row in top_states.iterrows():
                    print(f"  {row['State']}: {row['Production']:,.0f} thousand tonnes")
            
            # Save CSV
            csv_file = f"apeda_{category}_{fin_year}.csv"
            df.to_csv(csv_file, index=False)
            print(f"\n✓ Saved to: {csv_file}")
        
        time.sleep(1)  # Be nice to the API
    
    # Summary
    print(f"\n\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    summary_df = pd.DataFrame(results)
    print(summary_df.to_string(index=False))
    
    passed = sum(1 for r in results if r["Success"] == "✓")
    print(f"\n✓ Passed: {passed}/{len(results)}")


def test_specific_products():
    """Test specific products with their numeric codes"""
    
    print("\n" + "="*80)
    print("TESTING SPECIFIC PRODUCTS (Using Product Codes)")
    print("="*80)
    
    # Product codes from the HTML form
    products = [
        {"name": "Rice", "code": "1011", "category": "Agri"},
        {"name": "Wheat", "code": "1013", "category": "Agri"},
        {"name": "Maize", "code": "1009", "category": "Agri"},
        {"name": "Milk", "code": "1023", "category": "LiveStock"},
        {"name": "Mango", "code": "1050", "category": "Fruits"},
        {"name": "Potato", "code": "1083", "category": "Vegetables"},
        {"name": "Turmeric", "code": "1099", "category": "Spices"},
    ]
    
    fin_year = "2023-24"
    results = []
    
    for product in products:
        print(f"\n{'='*80}")
        print(f"PRODUCT: {product['name']} (Code: {product['code']}) - Category: {product['category']}")
        print(f"{'='*80}")
        
        # Try with specific category
        df = fetch_apeda_data(
            fin_year=fin_year,
            category=product['category'],
            product_code=product['code'],
            report_type="1"
        )
        
        success = len(df) > 0
        results.append({
            "Product": product['name'],
            "Code": product['code'],
            "Category": product['category'],
            "Success": "✓" if success else "✗",
            "Rows": len(df)
        })
        
        if success:
            print(f"\nTop 5 States:")
            if "Production" in df.columns and "State" in df.columns:
                top_states = df.nlargest(5, "Production")[["State", "Production"]]
                for idx, row in top_states.iterrows():
                    print(f"  {row['State']}: {row['Production']:,.0f} thousand tonnes")
        
        time.sleep(1)
    
    # Summary
    print(f"\n\n{'='*80}")
    print("PRODUCT TESTS SUMMARY")
    print(f"{'='*80}")
    summary_df = pd.DataFrame(results)
    print(summary_df.to_string(index=False))
    
    passed = sum(1 for r in results if r["Success"] == "✓")
    print(f"\n✓ Passed: {passed}/{len(results)}")


def test_report_types():
    """Test Summary vs Detailed report types"""
    
    print("\n" + "="*80)
    print("TESTING REPORT TYPES (Summary vs Detailed)")
    print("="*80)
    
    fin_year = "2023-24"
    category = "Agri"
    product_code = "1011"  # Rice
    
    for report_type in ["1", "2"]:
        report_name = "Summary" if report_type == "1" else "Detailed"
        print(f"\n{'='*80}")
        print(f"REPORT TYPE: {report_name} (Code: {report_type})")
        print(f"{'='*80}")
        
        df = fetch_apeda_data(
            fin_year=fin_year,
            category=category,
            product_code=product_code,
            report_type=report_type
        )
        
        if len(df) > 0:
            print(f"\nColumns: {list(df.columns)}")
            print(f"Shape: {df.shape}")
            print(f"\nFirst 3 rows:")
            print(df.head(3).to_string())
        
        time.sleep(1)


if __name__ == "__main__":
    print("\n" + "#"*80)
    print("# APEDA API COMPREHENSIVE TEST SUITE")
    print("# Using correct parameters from website form")
    print("#"*80)
    
    # Run all tests
    test_categories()
    test_specific_products()
    test_report_types()
    
    print("\n" + "#"*80)
    print("# ALL TESTS COMPLETED")
    print("#"*80)
