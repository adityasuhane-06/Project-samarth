"""
Get all 36 meteorological subdivisions from the historical rainfall API
"""

import requests
import pandas as pd

HISTORICAL_RAINFALL_URL = "https://api.data.gov.in/resource/440dbca7-86ce-4bf6-b1af-83af2855757e"
API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

def get_all_subdivisions():
    """Fetch enough records to see all 36 subdivisions"""
    
    print("\nFetching data to discover all 36 meteorological subdivisions...")
    
    all_subdivisions = set()
    limit = 10
    
    # Fetch multiple pages to get all 36 subdivisions
    # 36 subdivisions × 115 years (1901-2015) = 4,140 records
    # Need to fetch at least 360 records to see all subdivisions (36 × 10 years minimum)
    
    for offset in range(0, 400, limit):
        params = {
            'api-key': API_KEY,
            'format': 'json',
            'limit': limit,
            'offset': offset
        }
        
        try:
            response = requests.get(HISTORICAL_RAINFALL_URL, params=params, timeout=30)
            data = response.json()
            records = data.get('records', [])
            
            if not records:
                break
            
            df = pd.DataFrame(records)
            if 'subdivision' in df.columns:
                all_subdivisions.update(df['subdivision'].unique())
            
            print(f"  Offset {offset}: Found {len(all_subdivisions)} unique subdivisions so far...")
            
            if len(all_subdivisions) >= 36:
                print(f"\n✓ Found all 36 subdivisions!")
                break
                
        except Exception as e:
            print(f"Error at offset {offset}: {e}")
            break
    
    subdivisions_list = sorted(all_subdivisions)
    
    print(f"\n{'='*80}")
    print(f"ALL 36 METEOROLOGICAL SUBDIVISIONS")
    print(f"{'='*80}\n")
    
    for i, subdiv in enumerate(subdivisions_list, 1):
        print(f"{i:2d}. {subdiv}")
    
    # Save to file
    with open('meteorological_subdivisions.txt', 'w') as f:
        f.write("36 Meteorological Subdivisions of India\n")
        f.write("="*50 + "\n\n")
        for i, subdiv in enumerate(subdivisions_list, 1):
            f.write(f"{i:2d}. {subdiv}\n")
    
    print(f"\n✓ Saved to: meteorological_subdivisions.txt")
    
    return subdivisions_list


def fetch_subdivision_data(subdivision, year_start=None, year_end=None):
    """Fetch data for a specific subdivision"""
    
    print(f"\n{'='*80}")
    print(f"Fetching data for: {subdivision}")
    if year_start and year_end:
        print(f"Year range: {year_start} to {year_end}")
    print(f"{'='*80}")
    
    all_records = []
    limit = 10
    offset = 0
    
    for page in range(15):  # Up to 150 records (should cover 1901-2015)
        params = {
            'api-key': API_KEY,
            'format': 'json',
            'limit': limit,
            'offset': offset,
            'filters[subdivision]': subdivision
        }
        
        try:
            response = requests.get(HISTORICAL_RAINFALL_URL, params=params, timeout=30)
            data = response.json()
            records = data.get('records', [])
            
            if not records:
                break
            
            df_page = pd.DataFrame(records)
            all_records.append(df_page)
            
            offset += limit
            
            if len(records) < limit:
                break
                
        except Exception as e:
            print(f"Error: {e}")
            break
    
    if not all_records:
        print("✗ No data found")
        return pd.DataFrame()
    
    df = pd.concat(all_records, ignore_index=True)
    
    # Convert numeric columns
    for col in df.columns:
        if col not in ['subdivision']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Filter by year range if provided
    if year_start and year_end and 'year' in df.columns:
        df = df[(df['year'] >= year_start) & (df['year'] <= year_end)]
    
    df = df.sort_values('year') if 'year' in df.columns else df
    
    print(f"\n✓ Fetched {len(df)} records")
    
    if 'year' in df.columns:
        print(f"  Year range: {int(df['year'].min())} to {int(df['year'].max())}")
    
    if 'annual' in df.columns:
        print(f"\n📊 Rainfall Statistics:")
        print(f"  Average Annual: {df['annual'].mean():.2f} mm")
        print(f"  Maximum: {df['annual'].max():.2f} mm (Year: {int(df.loc[df['annual'].idxmax(), 'year'])})")
        print(f"  Minimum: {df['annual'].min():.2f} mm (Year: {int(df.loc[df['annual'].idxmin(), 'year'])})")
    
    # Save to CSV
    filename = f"{subdivision.replace(' ', '_').replace('&', 'and')}_rainfall.csv"
    df.to_csv(filename, index=False)
    print(f"\n✓ Saved to: {filename}")
    
    return df


if __name__ == "__main__":
    print("\n" + "="*80)
    print("DISCOVERING METEOROLOGICAL SUBDIVISIONS")
    print("="*80)
    
    # Get all subdivisions
    subdivisions = get_all_subdivisions()
    
    # Test with a few subdivisions
    print("\n\n" + "="*80)
    print("TESTING WITH SAMPLE SUBDIVISIONS")
    print("="*80)
    
    test_subdivisions = []
    
    # Find Punjab, Haryana, Maharashtra subdivisions
    for subdiv in subdivisions:
        if 'PUNJAB' in subdiv or 'HARYANA' in subdiv or 'MAHARASHTRA' in subdiv or 'KONKAN' in subdiv:
            test_subdivisions.append(subdiv)
    
    print(f"\nTesting with: {test_subdivisions}")
    
    for subdiv in test_subdivisions:
        df = fetch_subdivision_data(subdiv, year_start=2010, year_end=2015)
        
        if len(df) > 0 and 'annual' in df.columns:
            print(f"\n  Recent Years (2010-2015):")
            for idx, row in df.iterrows():
                if 'year' in df.columns:
                    print(f"    {int(row['year'])}: {row['annual']:.2f} mm")
    
    print("\n" + "="*80)
    print("DONE!")
    print("="*80)
