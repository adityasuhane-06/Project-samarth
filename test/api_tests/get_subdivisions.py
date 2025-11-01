"""
Quick script to get all 36 subdivision names by fetching a larger batch
"""

import requests
import pandas as pd

HISTORICAL_RAINFALL_URL = "https://api.data.gov.in/resource/440dbca7-86ce-4bf6-b1af-83af2855757e"
API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

# Fetch 1000 records at once (but API will limit to max available per page)
params = {
    'api-key': API_KEY,
    'format': 'json',
    'limit': 1000  # Request large batch
}

print("Fetching data to discover all subdivisions...")

try:
    response = requests.get(HISTORICAL_RAINFALL_URL, params=params, timeout=30)
    data = response.json()
    
    records = data.get('records', [])
    total = data.get('total', 0)
    count = data.get('count', 0)
    
    print(f"\nTotal records in API: {total}")
    print(f"Records fetched in this call: {count}")
    
    if records:
        df = pd.DataFrame(records)
        
        if 'subdivision' in df.columns:
            subdivisions = sorted(df['subdivision'].unique())
            
            print(f"\n{'='*80}")
            print(f"FOUND {len(subdivisions)} METEOROLOGICAL SUBDIVISIONS")
            print(f"{'='*80}\n")
            
            for i, subdiv in enumerate(subdivisions, 1):
                print(f"{i:2d}. {subdiv}")
            
            # Also show a sample record to see data structure
            print(f"\n{'='*80}")
            print("SAMPLE RECORD (showing data structure)")
            print(f"{'='*80}\n")
            
            sample = df.iloc[0]
            for col in df.columns:
                print(f"  {col:15s}: {sample[col]}")
            
            # Save subdivisions list
            with open('subdivisions_list.txt', 'w', encoding='utf-8') as f:
                for i, subdiv in enumerate(subdivisions, 1):
                    f.write(f"{i:2d}. {subdiv}\n")
            
            print(f"\n✓ Saved to: subdivisions_list.txt")
            
            # Now let's fetch Punjab data specifically
            print(f"\n{'='*80}")
            print("FETCHING PUNJAB DATA")
            print(f"{'='*80}")
            
            # Find Punjab subdivision
            punjab_subdivs = [s for s in subdivisions if 'PUNJAB' in s]
            
            if punjab_subdivs:
                print(f"\nPunjab subdivision(s) found: {punjab_subdivs}")
                
                for punjab_name in punjab_subdivs:
                    params_punjab = {
                        'api-key': API_KEY,
                        'format': 'json',
                        'limit': 1000,
                        'filters[subdivision]': punjab_name
                    }
                    
                    response_punjab = requests.get(HISTORICAL_RAINFALL_URL, params=params_punjab, timeout=30)
                    data_punjab = response_punjab.json()
                    records_punjab = data_punjab.get('records', [])
                    
                    if records_punjab:
                        df_punjab = pd.DataFrame(records_punjab)
                        
                        # Convert to numeric
                        for col in ['year', 'annual', 'jun', 'jul', 'aug', 'sep']:
                            if col in df_punjab.columns:
                                df_punjab[col] = pd.to_numeric(df_punjab[col], errors='coerce')
                        
                        df_punjab = df_punjab.sort_values('year')
                        
                        print(f"\n✓ Fetched {len(df_punjab)} years of data for {punjab_name}")
                        print(f"  Year range: {int(df_punjab['year'].min())} to {int(df_punjab['year'].max())}")
                        
                        if 'annual' in df_punjab.columns:
                            print(f"\n📊 Rainfall Statistics:")
                            print(f"  Average Annual: {df_punjab['annual'].mean():.2f} mm")
                            print(f"  Maximum: {df_punjab['annual'].max():.2f} mm (Year: {int(df_punjab.loc[df_punjab['annual'].idxmax(), 'year'])})")
                            print(f"  Minimum: {df_punjab['annual'].min():.2f} mm (Year: {int(df_punjab.loc[df_punjab['annual'].idxmin(), 'year'])})")
                            
                            # Show 2010-2015
                            recent = df_punjab[df_punjab['year'] >= 2010]
                            print(f"\n📅 Recent Years (2010-2015):")
                            for idx, row in recent.iterrows():
                                print(f"  {int(row['year'])}: Annual={row['annual']:.2f} mm, Monsoon (Jun-Sep)={row['jun']+row['jul']+row['aug']+row['sep']:.2f} mm")
                        
                        # Save to CSV
                        filename = f"punjab_rainfall_1901_2015.csv"
                        df_punjab.to_csv(filename, index=False)
                        print(f"\n✓ Saved complete Punjab data to: {filename}")
            else:
                print("\n⚠ Punjab subdivision not found in the list")
                print("Available subdivisions:", subdivisions)
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
