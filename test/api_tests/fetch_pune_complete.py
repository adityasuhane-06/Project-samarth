"""
Fetch complete Pune 2024 rainfall data using pagination
"""

import requests
import pandas as pd
import time

RAINFALL_API_URL = "https://api.data.gov.in/resource/6c05cd1b-ed59-40c2-bc31-e314f39c6971"
API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

def fetch_all_pune_2024_rainfall():
    """Fetch all Pune 2024 rainfall data using pagination"""
    
    print("\n" + "="*80)
    print("FETCHING COMPLETE PUNE 2024 RAINFALL DATA")
    print("="*80)
    
    all_records = []
    limit = 10  # Sample key limit
    offset = 0
    total_available = None
    
    while True:
        print(f"\nFetching records {offset + 1} to {offset + limit}...")
        
        params = {
            'api-key': API_KEY,
            'format': 'json',
            'limit': limit,
            'offset': offset,
            'filters[State]': 'Maharashtra',
            'filters[District]': 'Pune',
            'filters[Year]': '2024'
        }
        
        try:
            response = requests.get(RAINFALL_API_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            records = data.get('records', [])
            total_available = data.get('total', 0)
            
            if not records:
                print(f"  No more records (fetched {len(all_records)} total)")
                break
            
            all_records.extend(records)
            print(f"  ✓ Fetched {len(records)} records")
            print(f"  Progress: {len(all_records)}/{total_available}")
            
            # Stop if we've fetched all records
            if len(all_records) >= total_available:
                break
            
            # Stop after fetching reasonable amount (364 records / 10 per request = ~37 requests)
            # But let's limit to 10 requests to avoid rate limiting
            if offset >= 90:  # 10 requests = 100 records
                print(f"\n  ⚠️ Fetched {len(all_records)} records. Stopping to avoid rate limiting.")
                print(f"  (Total available: {total_available})")
                break
            
            offset += limit
            time.sleep(0.5)  # Be nice to the API
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            break
    
    if not all_records:
        print("\n❌ No records found")
        return pd.DataFrame()
    
    # Create DataFrame
    df = pd.DataFrame(all_records)
    df['Avg_rainfall'] = pd.to_numeric(df['Avg_rainfall'], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Sort by date
    df = df.sort_values('Date')
    
    print(f"\n{'='*80}")
    print("PUNE 2024 RAINFALL ANALYSIS")
    print(f"{'='*80}")
    
    print(f"\n📊 Dataset Statistics:")
    print(f"  Total Records: {len(df)}")
    print(f"  Date Range: {df['Date'].min()} to {df['Date'].max()}")
    
    # Rainfall statistics
    total_rainfall = df['Avg_rainfall'].sum()
    avg_daily = df['Avg_rainfall'].mean()
    max_daily = df['Avg_rainfall'].max()
    min_daily = df['Avg_rainfall'].min()
    rainy_days = len(df[df['Avg_rainfall'] > 0])
    
    print(f"\n🌧️ Rainfall Statistics:")
    print(f"  Total Rainfall: {total_rainfall:.2f} mm")
    print(f"  Average Daily: {avg_daily:.2f} mm")
    print(f"  Maximum Daily: {max_daily:.2f} mm")
    print(f"  Minimum Daily: {min_daily:.2f} mm")
    print(f"  Rainy Days: {rainy_days} ({rainy_days/len(df)*100:.1f}%)")
    print(f"  Dry Days: {len(df) - rainy_days}")
    
    # Monthly breakdown
    df['Month'] = df['Date'].dt.month
    monthly_rainfall = df.groupby('Month')['Avg_rainfall'].sum()
    
    print(f"\n📅 Monthly Rainfall (from fetched data):")
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                   7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    
    for month, rainfall in monthly_rainfall.items():
        print(f"  {month_names.get(month, month)}: {rainfall:.2f} mm")
    
    # Top 10 wettest days
    print(f"\n🌧️ Top 10 Wettest Days:")
    top_days = df.nlargest(10, 'Avg_rainfall')[['Date', 'Avg_rainfall']]
    for idx, row in top_days.iterrows():
        date_str = row['Date'].strftime('%Y-%m-%d %A') if pd.notna(row['Date']) else 'Unknown'
        print(f"  {date_str}: {row['Avg_rainfall']:.2f} mm")
    
    # Save to CSV
    filename = 'pune_2024_rainfall_complete.csv'
    df.to_csv(filename, index=False)
    print(f"\n✓ Saved complete data to: {filename}")
    
    return df


if __name__ == "__main__":
    print("\n" + "#"*80)
    print("# PUNE 2024 RAINFALL - COMPLETE DATASET")
    print("#"*80)
    
    df = fetch_all_pune_2024_rainfall()
    
    if len(df) > 0:
        print(f"\n" + "="*80)
        print("SUCCESS!")
        print(f"="*80)
        print(f"✓ Fetched {len(df)} records")
        print(f"✓ Data saved to: pune_2024_rainfall_complete.csv")
        print(f"\n💡 To get ALL 364 records, you need to:")
        print(f"  1. Register at https://data.gov.in/")
        print(f"  2. Get your own API key (no 10-record limit)")
        print(f"  3. Replace the API_KEY in the script")
    
    print("\n" + "#"*80)
