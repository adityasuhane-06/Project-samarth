"""
Test script for Daily District-wise Rainfall Data API from data.gov.in
Resource ID: 6c05cd1b-ed59-40c2-bc31-e314f39c6971
"""

import requests
import pandas as pd
import json
from datetime import datetime
import time

# API Configuration
RAINFALL_API_URL = "https://api.data.gov.in/resource/6c05cd1b-ed59-40c2-bc31-e314f39c6971"
API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"  # Sample key (10 records limit)

def fetch_rainfall_data(state=None, district=None, year=None, limit=100, offset=0):
    """
    Fetch rainfall data from data.gov.in API
    
    Parameters:
    - state: State name (e.g., "Maharashtra", "Punjab")
    - district: District name (e.g., "Pune", "Amritsar")
    - year: Year (e.g., 2024, 2023)
    - limit: Maximum records to return (default 100, sample key limited to 10)
    - offset: Number of records to skip
    
    Returns:
    - DataFrame with rainfall data
    """
    
    params = {
        'api-key': API_KEY,
        'format': 'json',
        'limit': limit,
        'offset': offset
    }
    
    # Add filters if provided
    filters = []
    if state:
        params['filters[state_name]'] = state
        filters.append(f"State: {state}")
    if district:
        params['filters[dist_name]'] = district
        filters.append(f"District: {district}")
    if year:
        params['filters[year]'] = year
        filters.append(f"Year: {year}")
    
    filter_str = ", ".join(filters) if filters else "No filters"
    
    print(f"\n{'='*80}")
    print(f"Fetching Rainfall Data")
    print(f"Filters: {filter_str}")
    print(f"Limit: {limit}, Offset: {offset}")
    print(f"{'='*80}")
    
    try:
        response = requests.get(RAINFALL_API_URL, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"\n✓ Response Status: {response.status_code}")
        
        # Save raw response
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        state_str = state.replace(" ", "_") if state else "All"
        district_str = district.replace(" ", "_") if district else "All"
        year_str = str(year) if year else "All"
        filename = f"rainfall_{state_str}_{district_str}_{year_str}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Raw response saved to: {filename}")
        
        # Extract records
        records = data.get('records', [])
        
        if not records:
            print("\n⚠ No records found")
            print(f"Total available: {data.get('total', 0)}")
            print(f"API Keys: {list(data.keys())}")
            return pd.DataFrame()
        
        df = pd.DataFrame(records)
        
        print(f"\n✓ Successfully fetched {len(df)} records")
        print(f"  Total available: {data.get('total', 'Unknown')}")
        print(f"  Columns: {list(df.columns)}")
        
        # Show sample data
        if len(df) > 0:
            print(f"\n📊 First record sample:")
            for col in df.columns[:8]:  # Show first 8 columns
                print(f"  {col}: {df[col].iloc[0]}")
        
        # Convert numeric columns
        numeric_cols = ['rainfall', 'year', 'actual_rainfall', 'normal_rainfall']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Save to CSV
        csv_filename = f"rainfall_{state_str}_{district_str}_{year_str}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\n✓ Saved to: {csv_filename}")
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching data: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


def test_pune_2024_rainfall():
    """Fetch 2024 rainfall data for Pune district"""
    
    print("\n" + "#"*80)
    print("# PUNE RAINFALL DATA - 2024")
    print("#"*80)
    
    df = fetch_rainfall_data(state="Maharashtra", district="PUNE", year=2024, limit=100)
    
    if len(df) > 0:
        print(f"\n{'='*80}")
        print("PUNE 2024 RAINFALL ANALYSIS")
        print(f"{'='*80}")
        
        # Show available columns
        print(f"\nAvailable columns: {list(df.columns)}")
        
        # Calculate statistics if rainfall column exists
        rainfall_col = None
        for col in ['rainfall', 'actual_rainfall', 'Rainfall']:
            if col in df.columns:
                rainfall_col = col
                break
        
        if rainfall_col:
            total_rainfall = df[rainfall_col].sum()
            avg_rainfall = df[rainfall_col].mean()
            max_rainfall = df[rainfall_col].max()
            min_rainfall = df[rainfall_col].min()
            
            print(f"\n📊 Rainfall Statistics for Pune 2024:")
            print(f"  Total Records: {len(df)}")
            print(f"  Total Rainfall: {total_rainfall:.2f} mm")
            print(f"  Average Rainfall: {avg_rainfall:.2f} mm")
            print(f"  Maximum Rainfall: {max_rainfall:.2f} mm")
            print(f"  Minimum Rainfall: {min_rainfall:.2f} mm")
            
            # Show top 10 wettest days
            if len(df) >= 10:
                print(f"\n🌧️ Top 10 Wettest Days in Pune 2024:")
                top_days = df.nlargest(10, rainfall_col)
                for idx, row in top_days.iterrows():
                    date_col = None
                    for col in ['date', 'Date', 'rainfall_date']:
                        if col in df.columns:
                            date_col = col
                            break
                    
                    if date_col:
                        print(f"  {row[date_col]}: {row[rainfall_col]:.2f} mm")
                    else:
                        print(f"  Record {idx}: {row[rainfall_col]:.2f} mm")
        
        # Show first 5 records
        print(f"\n📋 First 5 Records:")
        print(df.head(5).to_string())
        
    else:
        print("\n⚠️ No data found for Pune 2024")
        print("Trying without year filter to see available years...")
        
        # Try fetching without year to see what's available
        df_all = fetch_rainfall_data(state="Maharashtra", district="PUNE", limit=10)
        
        if len(df_all) > 0 and 'year' in df_all.columns:
            available_years = sorted(df_all['year'].dropna().unique())
            print(f"\n📅 Available years for Pune: {available_years}")


def test_multiple_locations():
    """Test rainfall data for multiple locations"""
    
    print("\n" + "#"*80)
    print("# TESTING MULTIPLE LOCATIONS")
    print("#"*80)
    
    test_cases = [
        {"name": "Pune 2024", "state": "Maharashtra", "district": "PUNE", "year": 2024},
        {"name": "Pune 2023", "state": "Maharashtra", "district": "PUNE", "year": 2023},
        {"name": "Mumbai 2024", "state": "Maharashtra", "district": "MUMBAI", "year": 2024},
        {"name": "Amritsar 2024", "state": "Punjab", "district": "AMRITSAR", "year": 2024},
        {"name": "Bangalore 2024", "state": "Karnataka", "district": "BANGALORE", "year": 2024},
    ]
    
    results = []
    
    for test in test_cases:
        print(f"\n{'#'*80}")
        print(f"# TEST: {test['name']}")
        print(f"{'#'*80}")
        
        df = fetch_rainfall_data(
            state=test['state'],
            district=test['district'],
            year=test['year'],
            limit=100
        )
        
        success = len(df) > 0
        
        rainfall_total = 0
        if success:
            rainfall_col = None
            for col in ['rainfall', 'actual_rainfall', 'Rainfall']:
                if col in df.columns:
                    rainfall_col = col
                    break
            
            if rainfall_col:
                rainfall_total = df[rainfall_col].sum()
        
        results.append({
            "Location": test['name'],
            "Success": "✓" if success else "✗",
            "Records": len(df),
            "Total Rainfall (mm)": f"{rainfall_total:.2f}" if success else "N/A"
        })
        
        time.sleep(1)  # Be nice to the API
    
    # Print summary
    print(f"\n\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    
    summary_df = pd.DataFrame(results)
    print(summary_df.to_string(index=False))


def explore_api_structure():
    """Explore the API structure with basic call"""
    
    print("\n" + "#"*80)
    print("# EXPLORING API STRUCTURE")
    print("#"*80)
    
    # Basic call with no filters to see structure
    df = fetch_rainfall_data(limit=10)
    
    if len(df) > 0:
        print(f"\n📋 Sample Records:")
        print(df.head(3).to_string())
        
        print(f"\n📊 Column Data Types:")
        print(df.dtypes)
        
        # Check for unique values in key columns
        for col in ['state_name', 'dist_name', 'year']:
            if col in df.columns:
                unique_vals = df[col].unique()
                print(f"\n{col}: {len(unique_vals)} unique values")
                if len(unique_vals) <= 10:
                    print(f"  Values: {list(unique_vals)}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("RAINFALL DATA API TEST SUITE")
    print("="*80)
    
    # First, explore the API structure
    explore_api_structure()
    
    # Main test: Pune 2024 rainfall
    test_pune_2024_rainfall()
    
    # Test multiple locations
    test_multiple_locations()
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED")
    print("="*80)
