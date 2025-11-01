"""
Explore available districts and years in the rainfall API
Then fetch Pune 2024 data with correct district name
"""

import requests
import pandas as pd
import json

RAINFALL_API_URL = "https://api.data.gov.in/resource/6c05cd1b-ed59-40c2-bc31-e314f39c6971"
API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

def fetch_maharashtra_districts():
    """Fetch sample data from Maharashtra to see district names"""
    
    print("\n" + "="*80)
    print("EXPLORING MAHARASHTRA DISTRICTS")
    print("="*80)
    
    params = {
        'api-key': API_KEY,
        'format': 'json',
        'limit': 100,
        'filters[State]': 'Maharashtra'
    }
    
    try:
        response = requests.get(RAINFALL_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        records = data.get('records', [])
        
        if records:
            df = pd.DataFrame(records)
            
            print(f"\n✓ Fetched {len(df)} records from Maharashtra")
            
            # Get unique districts
            if 'District' in df.columns:
                districts = sorted(df['District'].unique())
                print(f"\n📍 Found {len(districts)} districts:")
                for i, district in enumerate(districts, 1):
                    print(f"  {i}. {district}")
            
            # Get available years
            if 'Year' in df.columns:
                df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
                years = sorted(df['Year'].dropna().unique())
                print(f"\n📅 Available years: {[int(y) for y in years]}")
            
            # Check if Pune exists
            if 'District' in df.columns:
                pune_variations = [d for d in districts if 'pune' in d.lower() or 'poona' in d.lower()]
                if pune_variations:
                    print(f"\n✓ Pune district found as: {pune_variations}")
                else:
                    print(f"\n⚠ 'Pune' not found. Possible names: {districts[:10]}")
            
            # Save sample
            df.to_csv('maharashtra_rainfall_sample.csv', index=False)
            print(f"\n✓ Saved sample to: maharashtra_rainfall_sample.csv")
            
            return df
        else:
            print("\n⚠ No records found for Maharashtra")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return pd.DataFrame()


def fetch_pune_rainfall(year=2024):
    """Try different variations of Pune district name"""
    
    print(f"\n" + "="*80)
    print(f"SEARCHING FOR PUNE {year} RAINFALL DATA")
    print("="*80)
    
    pune_variations = [
        "Pune",
        "PUNE", 
        "Poona",
        "POONA"
    ]
    
    for district_name in pune_variations:
        print(f"\nTrying: State=Maharashtra, District={district_name}, Year={year}")
        
        params = {
            'api-key': API_KEY,
            'format': 'json',
            'limit': 100,
            'filters[State]': 'Maharashtra',
            'filters[District]': district_name,
            'filters[Year]': str(year)
        }
        
        try:
            response = requests.get(RAINFALL_API_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            records = data.get('records', [])
            total = data.get('total', 0)
            
            if records:
                print(f"  ✓ Found {len(records)} records (Total: {total})")
                
                df = pd.DataFrame(records)
                
                # Calculate rainfall stats
                if 'Avg_rainfall' in df.columns:
                    df['Avg_rainfall'] = pd.to_numeric(df['Avg_rainfall'], errors='coerce')
                    total_rainfall = df['Avg_rainfall'].sum()
                    avg_rainfall = df['Avg_rainfall'].mean()
                    max_rainfall = df['Avg_rainfall'].max()
                    
                    print(f"\n  📊 Rainfall Statistics:")
                    print(f"    Total Rainfall: {total_rainfall:.2f} mm")
                    print(f"    Average Daily: {avg_rainfall:.2f} mm")
                    print(f"    Maximum Daily: {max_rainfall:.2f} mm")
                    
                    # Save data
                    filename = f"pune_{year}_rainfall.csv"
                    df.to_csv(filename, index=False)
                    print(f"\n  ✓ Saved to: {filename}")
                    
                    # Show wettest days
                    if len(df) > 0:
                        print(f"\n  🌧️ Wettest Days:")
                        top_days = df.nlargest(min(10, len(df)), 'Avg_rainfall')
                        for idx, row in top_days.iterrows():
                            date = row.get('Date', 'Unknown')
                            rainfall = row.get('Avg_rainfall', 0)
                            print(f"    {date}: {rainfall:.2f} mm")
                
                return df
            else:
                print(f"  ✗ No records found (Total available: {total})")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    return pd.DataFrame()


def check_latest_year_available():
    """Check what's the most recent year available in the dataset"""
    
    print("\n" + "="*80)
    print("CHECKING LATEST AVAILABLE YEAR")
    print("="*80)
    
    params = {
        'api-key': API_KEY,
        'format': 'json',
        'limit': 100,
        'filters[State]': 'Maharashtra'
    }
    
    try:
        response = requests.get(RAINFALL_API_URL, params=params, timeout=30)
        data = response.json()
        records = data.get('records', [])
        
        if records:
            df = pd.DataFrame(records)
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
            
            latest_year = int(df['Year'].max())
            earliest_year = int(df['Year'].min())
            
            print(f"\n📅 Year Range: {earliest_year} to {latest_year}")
            
            # Get year distribution
            year_counts = df['Year'].value_counts().sort_index()
            print(f"\n📊 Records per year:")
            for year, count in year_counts.items():
                print(f"  {int(year)}: {count} records")
            
            return latest_year
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    print("\n" + "#"*80)
    print("# PUNE RAINFALL DATA EXPLORER")
    print("#"*80)
    
    # Step 1: Check latest available year
    latest_year = check_latest_year_available()
    
    # Step 2: Explore Maharashtra districts
    df_mh = fetch_maharashtra_districts()
    
    # Step 3: Try to fetch Pune 2024 data
    df_pune_2024 = fetch_pune_rainfall(year=2024)
    
    if len(df_pune_2024) == 0 and latest_year:
        print(f"\n⚠️ No data for 2024. Trying with year {latest_year}...")
        df_pune = fetch_pune_rainfall(year=latest_year)
    
    # Step 4: Try 2023, 2022, 2021 if 2024 not available
    if len(df_pune_2024) == 0:
        for year in [2023, 2022, 2021, 2020, 2019]:
            print(f"\n{'='*80}")
            print(f"Trying Year: {year}")
            print(f"{'='*80}")
            df = fetch_pune_rainfall(year=year)
            if len(df) > 0:
                print(f"\n✓ SUCCESS! Found data for {year}")
                break
    
    print("\n" + "#"*80)
    print("# EXPLORATION COMPLETED")
    print("#"*80)
