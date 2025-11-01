"""
Detailed test for Punjab state data (2019-2022)
Fetches state-wise and district-wise crop production data
"""

import requests
import json
from typing import Dict, List, Any
import pandas as pd


class PunjabDataFetcher:
    """Fetch detailed Punjab agricultural data"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
        self.base_url = "https://api.data.gov.in/resource"
        self.resource_id = "35be999b-0208-4354-b557-f6ca9a5355de"
        
    def fetch_punjab_by_year(self, year: str, limit: int = 100) -> Dict[str, Any]:
        """
        Fetch Punjab data for a specific year
        
        Args:
            year: Crop year (e.g., "2022", "2021", "2020", "2019")
            limit: Maximum records to fetch
        """
        url = f"{self.base_url}/{self.resource_id}"
        
        params = {
            'api-key': self.api_key,
            'format': 'json',
            'limit': limit,
            'filters[state_name]': 'Punjab',
            'filters[crop_year]': year
        }
        
        print(f"\n{'='*70}")
        print(f"📊 FETCHING PUNJAB DATA - YEAR {year}")
        print(f"{'='*70}")
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                records = data.get('records', [])
                
                print(f"✅ SUCCESS!")
                print(f"   Records fetched: {len(records)}")
                
                if records:
                    # Get unique districts
                    districts = set(r.get('district_name', 'N/A') for r in records)
                    crops = set(r.get('crop', 'N/A') for r in records)
                    seasons = set(r.get('season', 'N/A') for r in records)
                    
                    print(f"\n📍 Districts found: {len(districts)}")
                    print(f"   {', '.join(sorted(districts)[:10])}...")
                    print(f"\n🌾 Crops found: {len(crops)}")
                    print(f"   {', '.join(sorted(crops)[:10])}...")
                    print(f"\n📅 Seasons: {', '.join(sorted(seasons))}")
                    
                    # Show sample records
                    print(f"\n📋 SAMPLE RECORDS (first 5):")
                    for i, record in enumerate(records[:5], 1):
                        print(f"\n   {i}. District: {record.get('district_name', 'N/A')}")
                        print(f"      Crop: {record.get('crop', 'N/A')}")
                        print(f"      Season: {record.get('season', 'N/A')}")
                        print(f"      Area: {record.get('area_', 'N/A')} ha")
                        print(f"      Production: {record.get('production_', 'N/A')} tonnes")
                
                return data
            else:
                print(f"❌ ERROR: Status {response.status_code}")
                print(f"Response: {response.text}")
                return {'error': response.text, 'records': []}
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            return {'error': str(e), 'records': []}
    
    def fetch_punjab_all_years(self, years: List[str] = None) -> Dict[str, Any]:
        """Fetch Punjab data for multiple years"""
        if years is None:
            # Based on API data, using years that exist in dataset
            years = ['2015', '2014', '2013', '2012']
        
        all_data = {}
        
        print(f"\n{'#'*70}")
        print(f"# PUNJAB AGRICULTURAL DATA ANALYSIS (2019-2022)")
        print(f"# State-wise and District-wise Breakdown")
        print(f"{'#'*70}")
        
        for year in years:
            data = self.fetch_punjab_by_year(year)
            all_data[year] = data
            
            # Save individual year data
            self.save_to_file(data, f"punjab_{year}.json")
        
        return all_data
    
    def analyze_punjab_data(self, all_data: Dict[str, Any]):
        """Analyze and summarize Punjab data"""
        print(f"\n{'='*70}")
        print(f"📊 PUNJAB DATA ANALYSIS SUMMARY")
        print(f"{'='*70}")
        
        all_records = []
        for year, data in all_data.items():
            records = data.get('records', [])
            for record in records:
                record['fetch_year'] = year
                all_records.append(record)
        
        if not all_records:
            print("❌ No records found!")
            return
        
        # Create DataFrame for analysis
        df = pd.DataFrame(all_records)
        
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"   Total Records: {len(df)}")
        print(f"   Years Covered: {', '.join(sorted(all_data.keys()))}")
        
        if 'district_name' in df.columns:
            print(f"\n📍 DISTRICTS ({df['district_name'].nunique()} unique):")
            district_counts = df['district_name'].value_counts()
            for district, count in district_counts.head(10).items():
                print(f"   • {district}: {count} records")
        
        if 'crop' in df.columns:
            print(f"\n🌾 TOP CROPS ({df['crop'].nunique()} unique):")
            crop_counts = df['crop'].value_counts()
            for crop, count in crop_counts.head(10).items():
                print(f"   • {crop}: {count} records")
        
        if 'season' in df.columns:
            print(f"\n📅 SEASONS:")
            season_counts = df['season'].value_counts()
            for season, count in season_counts.items():
                print(f"   • {season}: {count} records")
        
        # Production analysis
        if 'production_' in df.columns:
            df['production_num'] = pd.to_numeric(df['production_'], errors='coerce')
            print(f"\n📊 PRODUCTION STATISTICS:")
            print(f"   Total Production: {df['production_num'].sum():,.0f} tonnes")
            print(f"   Average Production: {df['production_num'].mean():,.0f} tonnes")
            print(f"   Max Production: {df['production_num'].max():,.0f} tonnes")
        
        # Area analysis
        if 'area_' in df.columns:
            df['area_num'] = pd.to_numeric(df['area_'], errors='coerce')
            print(f"\n📏 AREA STATISTICS:")
            print(f"   Total Area: {df['area_num'].sum():,.0f} hectares")
            print(f"   Average Area: {df['area_num'].mean():,.0f} hectares")
        
        # Save consolidated data
        self.save_to_file({
            'summary': {
                'total_records': len(df),
                'years': sorted(all_data.keys()),
                'districts': sorted(df['district_name'].unique().tolist()) if 'district_name' in df.columns else [],
                'crops': sorted(df['crop'].unique().tolist()) if 'crop' in df.columns else [],
            },
            'records': all_records
        }, "punjab_consolidated_2019_2022.json")
        
        # Save as CSV for easy viewing
        csv_path = "C:\\Users\\Lenovo\\Desktop\\Project samarth\\test\\api_tests\\punjab_data_2019_2022.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n💾 CSV saved to: {csv_path}")
        
        return df
    
    def save_to_file(self, data: Dict[str, Any], filename: str):
        """Save data to JSON file"""
        try:
            filepath = f"C:\\Users\\Lenovo\\Desktop\\Project samarth\\test\\api_tests\\{filename}"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"   💾 Saved: {filename}")
        except Exception as e:
            print(f"   ❌ Error saving {filename}: {str(e)}")


def main():
    """Main execution function"""
    print(f"\n{'#'*70}")
    print(f"# PUNJAB STATE AGRICULTURAL DATA FETCHER")
    print(f"# Years: 2012-2015 (Most recent available in dataset)")
    print(f"# Analysis: State-wise and District-wise")
    print(f"{'#'*70}")
    
    fetcher = PunjabDataFetcher()
    
    # Fetch data for all years
    years = ['2015', '2014', '2013', '2012']
    all_data = fetcher.fetch_punjab_all_years(years)
    
    # Analyze the data
    df = fetcher.analyze_punjab_data(all_data)
    
    print(f"\n{'#'*70}")
    print(f"# DATA FETCHING COMPLETED")
    print(f"{'#'*70}")
    print(f"\n📁 FILES CREATED:")
    print(f"   • punjab_2015.json")
    print(f"   • punjab_2014.json")
    print(f"   • punjab_2013.json")
    print(f"   • punjab_2012.json")
    print(f"   • punjab_consolidated_2019_2022.json")
    print(f"   • punjab_data_2019_2022.csv")
    print(f"\n💡 TIP: Open the CSV file in Excel for easy viewing!")
    print(f"\n")


if __name__ == "__main__":
    main()
