"""
Test script for Historical Rainfall API (1901-2015)
Resource ID: 440dbca7-86ce-4bf6-b1af-83af2855757e
Area weighted monthly, seasonal and annual rainfall for 36 meteorological subdivisions
"""

import requests
import pandas as pd
import json
from datetime import datetime
import time

# API Configuration
HISTORICAL_RAINFALL_URL = "https://api.data.gov.in/resource/440dbca7-86ce-4bf6-b1af-83af2855757e"
API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"  # Sample key

def fetch_historical_rainfall(subdivision=None, year=None, limit=100, offset=0):
    """
    Fetch historical rainfall data (1901-2015) for meteorological subdivisions
    
    Parameters:
    - subdivision: Meteorological subdivision name (e.g., "Punjab", "Maharashtra", "Konkan & Goa")
    - year: Year (1901-2015)
    - limit: Maximum records to return
    - offset: Number of records to skip
    
    Returns:
    - DataFrame with historical rainfall data
    """
    
    params = {
        'api-key': API_KEY,
        'format': 'json',
        'limit': limit,
        'offset': offset
    }
    
    # Add filters if provided
    filters = []
    if subdivision:
        params['filters[subdivision]'] = subdivision
        filters.append(f"Subdivision: {subdivision}")
    if year:
        params['filters[year]'] = year
        filters.append(f"Year: {year}")
    
    filter_str = ", ".join(filters) if filters else "No filters"
    
    print(f"\n{'='*80}")
    print(f"Fetching Historical Rainfall Data (1901-2015)")
    print(f"Filters: {filter_str}")
    print(f"Limit: {limit}, Offset: {offset}")
    print(f"{'='*80}")
    
    try:
        response = requests.get(HISTORICAL_RAINFALL_URL, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"\n✓ Response Status: {response.status_code}")
        
        # Extract records
        records = data.get('records', [])
        
        if not records:
            print("\n⚠ No records found")
            print(f"Total available: {data.get('total', 0)}")
            return pd.DataFrame()
        
        df = pd.DataFrame(records)
        
        print(f"\n✓ Successfully fetched {len(df)} records")
        print(f"  Total available: {data.get('total', 'Unknown')}")
        print(f"  Columns: {list(df.columns)}")
        
        # Show sample data
        if len(df) > 0:
            print(f"\n📊 First record sample:")
            for col in list(df.columns)[:10]:  # Show first 10 columns
                print(f"  {col}: {df[col].iloc[0]}")
        
        # Save raw response
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        subdiv_str = subdivision.replace(" ", "_").replace("&", "and") if subdivision else "All"
        year_str = str(year) if year else "All"
        filename = f"historical_rainfall_{subdiv_str}_{year_str}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Raw response saved to: {filename}")
        
        # Save to CSV
        csv_filename = f"historical_rainfall_{subdiv_str}_{year_str}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"✓ Saved to: {csv_filename}")
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching data: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


def explore_subdivisions():
    """Explore available meteorological subdivisions"""
    
    print("\n" + "#"*80)
    print("# EXPLORING METEOROLOGICAL SUBDIVISIONS")
    print("#"*80)
    
    # Fetch sample data to see what subdivisions are available
    df = fetch_historical_rainfall(limit=100)
    
    if len(df) > 0:
        print(f"\n📍 Available columns: {list(df.columns)}")
        
        # Check for subdivision column
        subdiv_col = None
        for col in df.columns:
            if 'subdivision' in col.lower() or 'region' in col.lower() or 'state' in col.lower():
                subdiv_col = col
                break
        
        if subdiv_col:
            subdivisions = sorted(df[subdiv_col].unique())
            print(f"\n📍 Found {len(subdivisions)} meteorological subdivisions:")
            for i, subdiv in enumerate(subdivisions, 1):
                print(f"  {i}. {subdiv}")
        
        # Check year range
        year_col = None
        for col in df.columns:
            if 'year' in col.lower():
                year_col = col
                break
        
        if year_col:
            df[year_col] = pd.to_numeric(df[year_col], errors='coerce')
            years = sorted(df[year_col].dropna().unique())
            print(f"\n📅 Year range in sample: {int(min(years))} to {int(max(years))}")
        
        # Show rainfall columns
        rainfall_cols = [col for col in df.columns if 'rainfall' in col.lower() or 'rain' in col.lower() or any(month in col.lower() for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'annual', 'season'])]
        if rainfall_cols:
            print(f"\n🌧️ Rainfall-related columns:")
            for col in rainfall_cols:
                print(f"  - {col}")
        
        return df
    
    return pd.DataFrame()


def test_state_wise_rainfall():
    """Test fetching rainfall for specific states/subdivisions"""
    
    print("\n" + "#"*80)
    print("# TESTING STATE-WISE RAINFALL DATA")
    print("#"*80)
    
    # Common meteorological subdivisions (may need to adjust based on actual API data)
    test_subdivisions = [
        "Punjab",
        "Haryana Delhi & Chandigarh",
        "West Uttar Pradesh",
        "East Uttar Pradesh",
        "Madhya Maharashtra",
        "Konkan & Goa",
        "Marathwada",
        "Vidarbha",
        "Coastal Karnataka",
        "North Interior Karnataka",
        "South Interior Karnataka"
    ]
    
    results = []
    
    for subdiv in test_subdivisions[:5]:  # Test first 5 to avoid too many requests
        print(f"\n{'='*80}")
        print(f"TESTING: {subdiv}")
        print(f"{'='*80}")
        
        # Fetch data for recent years (2010-2015)
        df = fetch_historical_rainfall(subdivision=subdiv, limit=10)
        
        success = len(df) > 0
        
        if success:
            # Try to find annual rainfall column
            annual_col = None
            for col in df.columns:
                if 'annual' in col.lower():
                    annual_col = col
                    break
            
            avg_rainfall = "N/A"
            if annual_col:
                df[annual_col] = pd.to_numeric(df[annual_col], errors='coerce')
                avg_rainfall = f"{df[annual_col].mean():.2f} mm"
        
        results.append({
            "Subdivision": subdiv,
            "Success": "✓" if success else "✗",
            "Records": len(df),
            "Avg Annual Rainfall": avg_rainfall
        })
        
        time.sleep(1)  # Be nice to the API
    
    # Summary
    print(f"\n\n{'='*80}")
    print("STATE-WISE RAINFALL TEST SUMMARY")
    print(f"{'='*80}")
    
    summary_df = pd.DataFrame(results)
    print(summary_df.to_string(index=False))


def fetch_punjab_time_series():
    """Fetch complete time series for Punjab (1901-2015)"""
    
    print("\n" + "#"*80)
    print("# PUNJAB RAINFALL TIME SERIES (1901-2015)")
    print("#"*80)
    
    # Try different possible names for Punjab
    punjab_variations = ["Punjab", "PUNJAB", "Punjab Region"]
    
    for punjab_name in punjab_variations:
        print(f"\nTrying subdivision name: {punjab_name}")
        
        all_records = []
        limit = 10
        offset = 0
        
        # Fetch multiple pages
        for page in range(12):  # 12 pages = 120 records (should cover 115 years 1901-2015)
            df = fetch_historical_rainfall(subdivision=punjab_name, limit=limit, offset=offset)
            
            if len(df) == 0:
                if page == 0:
                    print(f"  ✗ No data found for '{punjab_name}'")
                break
            
            all_records.append(df)
            offset += limit
            
            if len(df) < limit:  # Last page
                break
            
            time.sleep(0.5)
        
        if all_records:
            combined_df = pd.concat(all_records, ignore_index=True)
            print(f"\n✓ Successfully fetched {len(combined_df)} records for {punjab_name}")
            
            # Analyze the data
            year_col = None
            for col in combined_df.columns:
                if 'year' in col.lower():
                    year_col = col
                    break
            
            if year_col:
                combined_df[year_col] = pd.to_numeric(combined_df[year_col], errors='coerce')
                combined_df = combined_df.sort_values(year_col)
                
                min_year = int(combined_df[year_col].min())
                max_year = int(combined_df[year_col].max())
                
                print(f"\n📅 Year Range: {min_year} to {max_year}")
                print(f"📊 Total Years: {max_year - min_year + 1}")
                
                # Find annual rainfall column
                annual_col = None
                for col in combined_df.columns:
                    if 'annual' in col.lower():
                        annual_col = col
                        break
                
                if annual_col:
                    combined_df[annual_col] = pd.to_numeric(combined_df[annual_col], errors='coerce')
                    
                    print(f"\n🌧️ Rainfall Statistics ({punjab_name}):")
                    print(f"  Average Annual: {combined_df[annual_col].mean():.2f} mm")
                    print(f"  Maximum Year: {combined_df[annual_col].max():.2f} mm in {combined_df.loc[combined_df[annual_col].idxmax(), year_col]:.0f}")
                    print(f"  Minimum Year: {combined_df[annual_col].min():.2f} mm in {combined_df.loc[combined_df[annual_col].idxmin(), year_col]:.0f}")
                    
                    # Show recent years (2010-2015)
                    recent = combined_df[combined_df[year_col] >= 2010]
                    if len(recent) > 0:
                        print(f"\n📊 Recent Years (2010-2015):")
                        for idx, row in recent.iterrows():
                            print(f"  {int(row[year_col])}: {row[annual_col]:.2f} mm")
                
                # Save complete time series
                filename = f"punjab_rainfall_1901_2015.csv"
                combined_df.to_csv(filename, index=False)
                print(f"\n✓ Saved complete time series to: {filename}")
                
                return combined_df
            
            return combined_df
    
    return pd.DataFrame()


if __name__ == "__main__":
    print("\n" + "="*80)
    print("HISTORICAL RAINFALL DATA API TEST SUITE (1901-2015)")
    print("="*80)
    
    # Step 1: Explore available subdivisions
    df_sample = explore_subdivisions()
    
    # Step 2: Test state-wise rainfall
    test_state_wise_rainfall()
    
    # Step 3: Fetch complete Punjab time series as example
    df_punjab = fetch_punjab_time_series()
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED")
    print("="*80)
    
    print("\n💡 This API provides:")
    print("  - Historical rainfall data from 1901 to 2015")
    print("  - 36 meteorological subdivisions covering all of India")
    print("  - Monthly, seasonal, and annual rainfall data")
    print("  - Perfect for long-term climate analysis and trends")
