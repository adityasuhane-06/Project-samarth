"""Data integration service for external APIs"""
import requests
import pandas as pd
from typing import Optional

from config.settings import settings


class DataGovIntegration:
    """Handles data fetching from data.gov.in and APEDA"""
    
    BASE_URL = "https://api.data.gov.in/resource"
    CROP_RESOURCE_ID = "35be999b-0208-4354-b557-f6ca9a5355de"
    DAILY_RAINFALL_RESOURCE_ID = "6c05cd1b-ed59-40c2-bc31-e314f39c6971"
    HISTORICAL_RAINFALL_RESOURCE_ID = "440dbca7-86ce-4bf6-b1af-83af2855757e"
    APEDA_URL = "https://agriexchange.apeda.gov.in/Production/IndiaCat/GetIndiaProductionCatObject"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.DATA_GOV_API_KEY
        self.session = requests.Session()
        self.use_real_api = settings.USE_REAL_API
        
    def fetch_crop_production_data(self) -> pd.DataFrame:
        """Fetch crop production dataset - tries real API first, falls back to sample data"""
        if self.use_real_api and self.api_key:
            try:
                print("DEBUG: Attempting to fetch real crop data from data.gov.in...")
                real_data = self._fetch_real_crop_data()
                if len(real_data) > 0:
                    print(f"DEBUG: Successfully fetched {len(real_data)} real crop records")
                    return pd.DataFrame(real_data)
                else:
                    print("DEBUG: No real data returned, using sample data")
            except Exception as e:
                print(f"DEBUG: Error fetching real crop data: {e}, using sample data")
        
        print("DEBUG: Using sample crop data")
        return pd.DataFrame(self._get_sample_crop_data())
    
    def fetch_rainfall_data(self) -> pd.DataFrame:
        """Fetch rainfall dataset from IMD - uses sample data for now"""
        try:
            sample_data = self._get_sample_rainfall_data()
            return pd.DataFrame(sample_data)
        except Exception as e:
            print(f"Error fetching rainfall data: {e}")
            return pd.DataFrame(self._get_sample_rainfall_data())
    
    def _fetch_real_crop_data(self, limit: int = 100) -> list:
        """Fetch real crop production data from data.gov.in API"""
        url = f"{self.BASE_URL}/{self.CROP_RESOURCE_ID}"
        
        # Fetch data for multiple states and recent years
        states = ['Punjab', 'Haryana', 'Karnataka', 'Maharashtra']
        years = ['2015', '2014', '2013', '2012', '2011', '2010']
        
        all_records = []
        
        for state in states:
            for year in years[:3]:  # Fetch 3 most recent years per state
                try:
                    params = {
                        'api-key': self.api_key,
                        'format': 'json',
                        'limit': limit,
                        'filters[state_name]': state,
                        'filters[crop_year]': year
                    }
                    
                    response = self.session.get(url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        records = data.get('records', [])
                        
                        # Normalize the field names to match our schema
                        for record in records:
                            crop_year = record.get('crop_year', 0)
                            # Format as YYYY-YY (e.g., 2014 becomes 2014-15)
                            crop_year_formatted = f"{crop_year}-{str(crop_year + 1)[-2:]}" if crop_year else ''
                            
                            normalized = {
                                'State_Name': record.get('state_name', ''),
                                'District_Name': record.get('district_name', ''),
                                'Crop_Year': crop_year_formatted,
                                'Season': record.get('season', ''),
                                'Crop': record.get('crop', ''),
                                'Area': float(record.get('area_', 0)) if record.get('area_') else 0,
                                'Production': float(record.get('production_', 0)) if record.get('production_') else 0
                            }
                            all_records.append(normalized)
                        
                        print(f"DEBUG: Fetched {len(records)} records for {state} {year}")
                        
                except Exception as e:
                    print(f"DEBUG: Error fetching {state} {year}: {e}")
                    continue
        
        return all_records
    
    def _get_sample_crop_data(self) -> list:
        """Sample crop production data"""
        return [
            {'State_Name': 'Punjab', 'District_Name': 'Amritsar', 'Crop_Year': '2022-23', 
             'Season': 'Kharif', 'Crop': 'Rice', 'Area': 125000, 'Production': 550000},
            {'State_Name': 'Punjab', 'District_Name': 'Ludhiana', 'Crop_Year': '2022-23', 
             'Season': 'Kharif', 'Crop': 'Rice', 'Area': 145000, 'Production': 635000},
            {'State_Name': 'Punjab', 'District_Name': 'Amritsar', 'Crop_Year': '2022-23', 
             'Season': 'Rabi', 'Crop': 'Wheat', 'Area': 185000, 'Production': 925000},
            {'State_Name': 'Haryana', 'District_Name': 'Karnal', 'Crop_Year': '2022-23', 
             'Season': 'Kharif', 'Crop': 'Rice', 'Area': 98000, 'Production': 420000},
            {'State_Name': 'Haryana', 'District_Name': 'Hisar', 'Crop_Year': '2022-23', 
             'Season': 'Kharif', 'Crop': 'Rice', 'Area': 76000, 'Production': 298000},
            {'State_Name': 'Punjab', 'District_Name': 'Amritsar', 'Crop_Year': '2021-22', 
             'Season': 'Kharif', 'Crop': 'Rice', 'Area': 122000, 'Production': 530000},
            {'State_Name': 'Punjab', 'District_Name': 'Ludhiana', 'Crop_Year': '2021-22', 
             'Season': 'Kharif', 'Crop': 'Rice', 'Area': 140000, 'Production': 610000},
            {'State_Name': 'Haryana', 'District_Name': 'Karnal', 'Crop_Year': '2021-22', 
             'Season': 'Kharif', 'Crop': 'Rice', 'Area': 95000, 'Production': 405000},
            {'State_Name': 'Punjab', 'District_Name': 'Patiala', 'Crop_Year': '2022-23', 
             'Season': 'Kharif', 'Crop': 'Maize', 'Area': 45000, 'Production': 180000},
            {'State_Name': 'Haryana', 'District_Name': 'Ambala', 'Crop_Year': '2022-23', 
             'Season': 'Kharif', 'Crop': 'Maize', 'Area': 38000, 'Production': 152000},
        ]
    
    def _get_sample_rainfall_data(self) -> list:
        """Sample rainfall data"""
        return [
            {'State': 'Punjab', 'Year': 2022, 'Annual_Rainfall': 645.2, 'Monsoon_Rainfall': 487.3},
            {'State': 'Punjab', 'Year': 2021, 'Annual_Rainfall': 612.8, 'Monsoon_Rainfall': 465.1},
            {'State': 'Punjab', 'Year': 2020, 'Annual_Rainfall': 598.4, 'Monsoon_Rainfall': 442.7},
            {'State': 'Haryana', 'Year': 2022, 'Annual_Rainfall': 558.7, 'Monsoon_Rainfall': 423.4},
            {'State': 'Haryana', 'Year': 2021, 'Annual_Rainfall': 542.3, 'Monsoon_Rainfall': 408.9},
            {'State': 'Haryana', 'Year': 2020, 'Annual_Rainfall': 524.1, 'Monsoon_Rainfall': 395.2},
            {'State': 'Maharashtra', 'Year': 2022, 'Annual_Rainfall': 1124.5, 'Monsoon_Rainfall': 945.8},
            {'State': 'Maharashtra', 'Year': 2021, 'Annual_Rainfall': 1098.3, 'Monsoon_Rainfall': 918.7},
        ]
    
    def fetch_apeda_data(self, fin_year: str, category: str = "All", 
                        product_code: str = "All", report_type: str = "1") -> pd.DataFrame:
        """Fetch production data from APEDA API (2019-2024)"""
        payload = {
            "Category": category,
            "Financial_Year": fin_year,
            "product_code": product_code,
            "ReportType": report_type
        }
        
        print(f"DEBUG: fetch_apeda_data called with payload: {payload}")
        
        try:
            print(f"DEBUG: Making POST request to {self.APEDA_URL}")
            response = self.session.post(
                self.APEDA_URL,
                json=payload,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                timeout=30
            )
            print(f"DEBUG: Response status code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            
            print(f"DEBUG: Response data type: {type(data)}, length: {len(data) if isinstance(data, list) else 'N/A'}")
            
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
                
                df["Financial_Year"] = fin_year
                df["Category"] = category
                df["Product_Code"] = product_code
                
                if "Production" in df.columns:
                    df["Production"] = pd.to_numeric(df["Production"], errors="coerce")
                
                print(f"DEBUG: Returning DataFrame with {len(df)} rows")
                return df
            
            print(f"DEBUG: No data returned from APEDA API (empty or invalid response)")
            return pd.DataFrame()
            
        except Exception as e:
            print(f"DEBUG: Error fetching APEDA data: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def fetch_daily_rainfall(self, state: Optional[str] = None, 
                           district: Optional[str] = None,
                           year: Optional[int] = None, 
                           limit: int = 100) -> pd.DataFrame:
        """Fetch daily district-wise rainfall data (2019-2024)"""
        url = f"{self.BASE_URL}/{self.DAILY_RAINFALL_RESOURCE_ID}"
        
        params = {
            'api-key': self.api_key,
            'format': 'json',
            'limit': limit
        }
        
        if state:
            params['filters[State]'] = state
        if district:
            params['filters[District]'] = district
        if year:
            params['filters[Year]'] = str(year)
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            records = data.get('records', [])
            if records:
                df = pd.DataFrame(records)
                
                # Convert numeric columns
                for col in ['Avg_rainfall', 'Year']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            print(f"DEBUG: Error fetching daily rainfall: {e}")
            return pd.DataFrame()
    
    def fetch_historical_rainfall(self, subdivision: Optional[str] = None,
                                 year: Optional[int] = None,
                                 limit: int = 100) -> pd.DataFrame:
        """Fetch historical state-wise rainfall data (1901-2015)"""
        url = f"{self.BASE_URL}/{self.HISTORICAL_RAINFALL_RESOURCE_ID}"
        
        params = {
            'api-key': self.api_key,
            'format': 'json',
            'limit': limit
        }
        
        if subdivision:
            params['filters[subdivision]'] = subdivision
        if year:
            params['filters[year]'] = str(year)
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            records = data.get('records', [])
            if records:
                df = pd.DataFrame(records)
                
                # Convert numeric columns
                for col in df.columns:
                    if col not in ['subdivision']:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            print(f"DEBUG: Error fetching historical rainfall: {e}")
            return pd.DataFrame()
