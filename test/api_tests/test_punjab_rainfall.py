"""
Test different possible names for Punjab in the historical rainfall API
"""

import requests
import pandas as pd

HISTORICAL_RAINFALL_URL = "https://api.data.gov.in/resource/440dbca7-86ce-4bf6-b1af-83af2855757e"
API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

# Possible variations of Punjab and other states
test_names = [
    "PUNJAB",
    "Punjab",
    "HARYANA CHANDIGARH & DELHI",
    "HARYANA DELHI & CHANDIGARH",
    "WEST UTTAR PRADESH",
    "EAST UTTAR PRADESH", 
    "MADHYA MAHARASHTRA",
    "KONKAN & GOA",
    "VIDARBHA",
    "MARATHWADA"
]

print("Testing subdivision names...")
print("="*80)

found_subdivisions = []

for name in test_names:
    params = {
        'api-key': API_KEY,
        'format': 'json',
        'limit': 10,
        'filters[subdivision]': name
    }
    
    try:
        response = requests.get(HISTORICAL_RAINFALL_URL, params=params, timeout=30)
        data = response.json()
        
        records = data.get('records', [])
        total = data.get('total', 0)
        
        if total > 0:
            print(f"✓ {name:40s} - Found {total} records")
            found_subdivisions.append(name)
            
            # Show sample data
            if records:
                df = pd.DataFrame(records)
                if 'year' in df.columns and 'annual' in df.columns:
                    df['year'] = pd.to_numeric(df['year'], errors='coerce')
                    df['annual'] = pd.to_numeric(df['annual'], errors='coerce')
                    print(f"  Year range: {int(df['year'].min())}-{int(df['year'].max())}, Avg annual rainfall: {df['annual'].mean():.2f} mm")
        else:
            print(f"✗ {name:40s} - Not found")
            
    except Exception as e:
        print(f"✗ {name:40s} - Error: {e}")

print(f"\n{'='*80}")
print(f"SUMMARY: Found {len(found_subdivisions)} subdivisions")
print(f"{'='*80}")

for subdiv in found_subdivisions:
    print(f"  - {subdiv}")

# Now fetch complete data for Punjab if found
if "PUNJAB" in found_subdivisions:
    print(f"\n{'='*80}")
    print("FETCHING COMPLETE PUNJAB DATA (1901-2015)")
    print(f"{'='*80}")
    
    all_records = []
    for offset in range(0, 120, 10):  # 115 years, 10 records per page
        params = {
            'api-key': API_KEY,
            'format': 'json',
            'limit': 10,
            'offset': offset,
            'filters[subdivision]': 'PUNJAB'
        }
        
        response = requests.get(HISTORICAL_RAINFALL_URL, params=params, timeout=30)
        data = response.json()
        records = data.get('records', [])
        
        if not records:
            break
        
        all_records.extend(records)
        print(f"  Fetched {len(all_records)} records...")
    
    if all_records:
        df = pd.DataFrame(all_records)
        
        # Convert to numeric
        for col in df.columns:
            if col != 'subdivision':
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.sort_values('year')
        
        print(f"\n✓ Complete! Fetched {len(df)} years")
        print(f"  Year range: {int(df['year'].min())} to {int(df['year'].max())}")
        
        # Statistics
        print(f"\n📊 PUNJAB RAINFALL STATISTICS (1901-2015):")
        print(f"  Average Annual: {df['annual'].mean():.2f} mm")
        print(f"  Maximum: {df['annual'].max():.2f} mm (Year: {int(df.loc[df['annual'].idxmax(), 'year'])})")
        print(f"  Minimum: {df['annual'].min():.2f} mm (Year: {int(df.loc[df['annual'].idxmin(), 'year'])})")
        
        # Recent years
        recent = df[df['year'] >= 2010]
        print(f"\n📅 Recent Years (2010-2015):")
        for idx, row in recent.iterrows():
            monsoon = row['jun'] + row['jul'] + row['aug'] + row['sep']
            print(f"  {int(row['year'])}: Annual={row['annual']:.2f} mm, Monsoon={monsoon:.2f} mm")
        
        # Monthly averages
        print(f"\n📊 Monthly Average Rainfall (115-year average):")
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        for month, name in zip(months, month_names):
            if month in df.columns:
                print(f"  {name}: {df[month].mean():.2f} mm")
        
        # Save
        df.to_csv('PUNJAB_rainfall_1901_2015.csv', index=False)
        print(f"\n✓ Saved to: PUNJAB_rainfall_1901_2015.csv")
