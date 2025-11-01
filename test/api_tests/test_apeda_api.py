"""
Test script for APEDA (Agricultural and Processed Food Products Export Development Authority) API
Tests fetching production data from agriexchange.apeda.gov.in
"""

import requests
import pandas as pd
import json
from datetime import datetime

APEDA_URL = "https://agriexchange.apeda.gov.in/Production/IndiaCat/GetIndiaProductionCatObject"

def fetch_apeda_production(fin_year: str, category: str = "All", product_code: str = "All", report_type: str = "1") -> pd.DataFrame:
    """
    Fetch production data from APEDA API
    
    Parameters:
    - fin_year: Financial year like '2023-24'
    - category: 'All' or specific category like 'Cereals', 'Pulses', etc.
    - product_code: 'All' or specific product like 'Wheat', 'Rice', or internal code like '1101'
    - report_type: '1' = summary/state level
    
    Returns:
    - DataFrame with production data by state
    """
    payload = {
        "Category": category,
        "Financial_Year": fin_year,
        "product_code": product_code,
        "ReportType": report_type
    }

    print(f"\n{'='*60}")
    print(f"Fetching APEDA data:")
    print(f"  Financial Year: {fin_year}")
    print(f"  Category: {category}")
    print(f"  Product Code: {product_code}")
    print(f"  Report Type: {report_type}")
    print(f"{'='*60}")

    try:
        r = requests.post(
            APEDA_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30
        )
        r.raise_for_status()
        data = r.json()

        print(f"\n✓ Response Status: {r.status_code}")
        print(f"✓ Response received successfully")
        
        # Save raw response for inspection
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"apeda_{category}_{fin_year}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Raw response saved to: {filename}")

        # Inspect the JSON structure
        print(f"\n📊 Response structure:")
        print(f"  Type: {type(data)}")
        if isinstance(data, dict):
            print(f"  Keys: {list(data.keys())}")
            
        # Try to extract rows from various possible structures
        rows = None
        if isinstance(data, list):
            rows = data
            print(f"  Direct list with {len(rows)} items")
        elif isinstance(data, dict):
            if "data" in data:
                rows = data["data"]
                print(f"  Found 'data' key with {len(rows) if isinstance(rows, list) else 'non-list'} items")
            elif "records" in data:
                rows = data["records"]
                print(f"  Found 'records' key with {len(rows) if isinstance(rows, list) else 'non-list'} items")
            elif "result" in data:
                rows = data["result"]
                print(f"  Found 'result' key with {len(rows) if isinstance(rows, list) else 'non-list'} items")
            else:
                # Try to find the first list value
                for key, value in data.items():
                    if isinstance(value, list) and len(value) > 0:
                        rows = value
                        print(f"  Found list in key '{key}' with {len(rows)} items")
                        break

        if not rows or not isinstance(rows, list) or len(rows) == 0:
            print("\n⚠ WARNING: Could not find data rows in response")
            print("Please check the saved JSON file to understand the response structure")
            return pd.DataFrame()

        df = pd.DataFrame(rows)
        print(f"\n✓ Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
        print(f"  Columns: {list(df.columns)}")

        # Show sample of first row
        if len(df) > 0:
            print(f"\n📋 First row sample:")
            for col in df.columns[:5]:  # Show first 5 columns
                print(f"  {col}: {df[col].iloc[0]}")

        # Normalize numeric columns if they come as strings
        for col in df.columns:
            if col.lower() in ["production", "percent share", "percent_share", "quantity", "qty", "area"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Clean footer rows like 'Total' or 'Source'
        if "State" in df.columns:
            original_len = len(df)
            df = df[~df["State"].str.contains("Total", case=False, na=False)]
            df = df[~df["State"].str.contains("Source", case=False, na=False)]
            if len(df) < original_len:
                print(f"✓ Cleaned {original_len - len(df)} footer rows (Total/Source)")

        # Rename to canonical schema
        rename_map = {}
        for c in df.columns:
            cl = c.lower().strip()
            if cl.startswith("state"):
                rename_map[c] = "State"
            elif "production" in cl:
                rename_map[c] = "Production_000_tonnes"
            elif "percent" in cl:
                rename_map[c] = "Percent_Share"
        
        if rename_map:
            df = df.rename(columns=rename_map)
            print(f"✓ Renamed columns: {rename_map}")

        df["Financial_Year"] = fin_year
        df["Category"] = category
        df["Product_Code"] = product_code

        return df.reset_index(drop=True)

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching data: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


def run_tests():
    """Run various tests on APEDA API"""
    
    print("\n" + "="*70)
    print("APEDA API TEST SUITE")
    print("="*70)
    
    tests = [
        {
            "name": "Test 1: Recent year - All categories",
            "fin_year": "2023-24",
            "category": "All",
            "product_code": "All"
        },
        {
            "name": "Test 2: Cereals - 2022-23",
            "fin_year": "2022-23",
            "category": "Cereals",
            "product_code": "All"
        },
        {
            "name": "Test 3: Rice specific - 2022-23",
            "fin_year": "2022-23",
            "category": "Cereals",
            "product_code": "Rice"
        },
        {
            "name": "Test 4: Wheat specific - 2022-23",
            "fin_year": "2022-23",
            "category": "Cereals",
            "product_code": "Wheat"
        },
        {
            "name": "Test 5: Older year - 2020-21",
            "fin_year": "2020-21",
            "category": "All",
            "product_code": "All"
        }
    ]
    
    results = []
    
    for i, test in enumerate(tests, 1):
        print(f"\n\n{'#'*70}")
        print(f"# {test['name']}")
        print(f"{'#'*70}")
        
        df = fetch_apeda_production(
            fin_year=test["fin_year"],
            category=test["category"],
            product_code=test["product_code"]
        )
        
        success = len(df) > 0
        results.append({
            "Test": test["name"],
            "Success": "✓" if success else "✗",
            "Rows": len(df),
            "Columns": len(df.columns) if success else 0
        })
        
        if success:
            print(f"\n✓ TEST PASSED")
            print(f"\nData Summary:")
            print(f"  Total Rows: {len(df)}")
            print(f"  Columns: {list(df.columns)}")
            
            # Show top 5 states by production if available
            if "Production_000_tonnes" in df.columns and "State" in df.columns:
                top_states = df.nlargest(5, "Production_000_tonnes")[["State", "Production_000_tonnes"]]
                print(f"\n  Top 5 States by Production:")
                for idx, row in top_states.iterrows():
                    print(f"    {row['State']}: {row['Production_000_tonnes']:,.0f} thousand tonnes")
            
            # Save to CSV
            csv_filename = f"apeda_{test['fin_year']}_{test['category']}.csv"
            df.to_csv(csv_filename, index=False)
            print(f"\n  Saved to: {csv_filename}")
        else:
            print(f"\n✗ TEST FAILED - No data returned")
        
        # Small delay between requests
        import time
        time.sleep(1)
    
    # Print summary
    print(f"\n\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")
    
    summary_df = pd.DataFrame(results)
    print(summary_df.to_string(index=False))
    
    passed = sum(1 for r in results if r["Success"] == "✓")
    print(f"\n✓ Passed: {passed}/{len(results)}")
    print(f"✗ Failed: {len(results) - passed}/{len(results)}")


if __name__ == "__main__":
    run_tests()
