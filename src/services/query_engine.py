"""Query engine for executing queries on datasets"""
import pandas as pd
from typing import Tuple, List, Dict, Any, Optional

from services.data_integration import DataGovIntegration


class DataQueryEngine:
    """Executes queries on the integrated datasets"""
    
    def __init__(self, crop_data: pd.DataFrame, rainfall_data: pd.DataFrame, 
                 data_gov_integration: Optional[DataGovIntegration] = None):
        self.crop_df = crop_data
        self.rainfall_df = rainfall_data
        self.data_gov = data_gov_integration or DataGovIntegration()
    
    def execute_query(self, params: dict) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
        """Execute complete query across all needed datasets"""
        all_results = {}
        all_sources = []
        
        data_needed = params.get('data_needed', [])
        
        # District-wise crop production (data.gov.in, 2013-2014)
        if 'crop_production' in data_needed:
            crop_results, crop_sources = self.query_crop_production(params)
            all_results['crop_production'] = crop_results
            all_sources.extend(crop_sources)
        
        # APEDA production data (2019-2024)
        if 'apeda_production' in data_needed:
            apeda_results, apeda_sources = self.query_apeda(params)
            all_results['apeda_production'] = apeda_results
            all_sources.extend(apeda_sources)
        
        # Sample rainfall data (fallback)
        if 'rainfall' in data_needed:
            rainfall_results, rainfall_sources = self.query_rainfall(params)
            all_results['rainfall'] = rainfall_results
            all_sources.extend(rainfall_sources)
        
        # Daily district-wise rainfall (2019-2024)
        if 'daily_rainfall' in data_needed:
            daily_rainfall_results, daily_sources = self.query_daily_rainfall(params)
            all_results['daily_rainfall'] = daily_rainfall_results
            all_sources.extend(daily_sources)
        
        # Historical state-wise rainfall (1901-2015)
        if 'historical_rainfall' in data_needed:
            historical_results, historical_sources = self.query_historical_rainfall(params)
            all_results['historical_rainfall'] = historical_results
            all_sources.extend(historical_sources)
        
        return all_results, all_sources
    
    def query_crop_production(self, params: dict) -> Tuple[List[Dict], List[Dict]]:
        """Query crop production data based on parameters"""
        df = self.crop_df.copy()
        results = []
        sources = []
        
        # Store available years for error messages
        all_available_years = sorted(df['Crop_Year'].unique().tolist()) if len(df) > 0 else []
        
        # Apply filters (case-insensitive)
        if params.get('states'):
            states_lower = [s.lower() for s in params['states']]
            df = df[df['State_Name'].str.lower().isin(states_lower)]
        
        if params.get('districts'):
            districts_lower = [d.lower() for d in params['districts']]
            df = df[df['District_Name'].str.lower().isin(districts_lower)]
            
        if params.get('crops'):
            crops_lower = [c.lower() for c in params['crops']]
            df = df[df['Crop'].str.lower().isin(crops_lower)]
        
        if params.get('years'):
            year_filters = self._process_year_filters(params['years'], df)
            if year_filters:
                df = df[df['Crop_Year'].str.split('-').str[0].isin(year_filters)]
                print(f"DEBUG: Filtered to {len(df)} records for years: {sorted(year_filters)}")
        
        # Perform aggregation
        if params.get('aggregation') == 'top':
            top_crops = df.groupby(['State_Name', 'Crop'])['Production'].sum().reset_index()
            top_crops = top_crops.sort_values('Production', ascending=False)
            results.append({
                'type': 'top_crops',
                'data': top_crops.head(10).to_dict('records')
            })
        elif params.get('aggregation') == 'average':
            avg_data = df.groupby('State_Name').agg({
                'Production': 'mean',
                'Area': 'mean'
            }).reset_index()
            results.append({
                'type': 'averages',
                'data': avg_data.to_dict('records')
            })
        else:
            # Add metadata about available years if no data found
            metadata = {
                'available_years': all_available_years if all_available_years else ['No data available'],
                'note': f"Dataset contains data for years: {', '.join(all_available_years)}" if all_available_years else "No data available"
            }
            
            results.append({
                'type': 'crop_data',
                'data': df.to_dict('records'),
                'metadata': metadata
            })
        
        sources.append({
            'dataset': 'District-wise Crop Production Statistics',
            'source': 'data.gov.in - Ministry of Agriculture',
            'url': 'https://www.data.gov.in/catalog/district-wise-season-wise-crop-production-statistics'
        })
        
        return results, sources
    
    def query_rainfall(self, params: dict) -> Tuple[List[Dict], List[Dict]]:
        """Query rainfall data based on parameters"""
        df = self.rainfall_df.copy()
        results = []
        sources = []
        
        # Apply filters (case-insensitive)
        if params.get('states'):
            states_lower = [s.lower() for s in params['states']]
            df = df[df['State'].str.lower().isin(states_lower)]
        
        if params.get('years'):
            year_ints = self._convert_years_to_int(params['years'], df, 'Year')
            if year_ints:
                df = df[df['Year'].isin(year_ints)]
                print(f"DEBUG: Filtered to {len(df)} records for years: {sorted(year_ints)}")
        
        # Track which years were actually used
        years_used = sorted(df['Year'].unique().tolist()) if len(df) > 0 else []
        
        # Check if we have data after filtering
        if len(df) == 0:
            results.append({
                'type': 'rainfall_data',
                'data': [],
                'years_used': years_used
            })
        elif params.get('aggregation') == 'average':
            avg_rainfall = df.groupby('State').agg({
                'Annual_Rainfall': 'mean',
                'Monsoon_Rainfall': 'mean'
            }).reset_index()
            results.append({
                'type': 'average_rainfall',
                'data': avg_rainfall.to_dict('records'),
                'years_used': years_used,
                'note': f"Averages calculated from {len(years_used)} years: {', '.join(map(str, years_used))}"
            })
        else:
            results.append({
                'type': 'rainfall_data',
                'data': df.to_dict('records'),
                'years_used': years_used
            })
        
        sources.append({
            'dataset': 'Rainfall in India',
            'source': 'data.gov.in - India Meteorological Department (IMD)',
            'url': 'https://www.data.gov.in/catalog/rainfall-india'
        })
        
        return results, sources
    
    def query_apeda(self, params: dict) -> Tuple[List[Dict], List[Dict]]:
        """Query APEDA production data (2019-2024)"""
        results = []
        sources = []
        
        print("DEBUG: query_apeda called with params:", params)
        
        # Map crop names to APEDA product codes
        crop_to_code = {
            'rice': '1011', 'wheat': '1013', 'maize': '1009', 'bajra': '1010',
            'jowar': '1012', 'barley': '1014', 'milk': '1023', 'mango': '1050',
            'banana': '1051', 'apple': '1052', 'potato': '1083', 'onion': '1084',
            'tomato': '1085', 'turmeric': '1099', 'chilli': '1100', 'coriander': '1101'
        }
        
        # Determine years to query
        years = params.get('years', [])
        if not years:
            years = ['2023-24']  # Default to most recent year
        
        # Ensure years are in financial year format
        fin_years = self._convert_to_financial_years(years)
        print(f"DEBUG: Financial years: {fin_years}")
        
        # Determine category and product code
        category = params.get('apeda_category', 'All')
        product_code = params.get('product_code')
        
        # If specific crops mentioned, use product codes
        crops = params.get('crops', [])
        if crops and (product_code is None or product_code == 'All'):
            crop_name = crops[0].lower()
            if crop_name in crop_to_code:
                product_code = crop_to_code[crop_name]
                print(f"DEBUG: Mapped crop '{crop_name}' to product code '{product_code}'")
        
        # Ensure product_code is a string, not None
        if product_code is None:
            product_code = "All"
        
        print(f"DEBUG: Category: {category}, Product Code: {product_code}")
        
        all_data = []
        for fin_year in fin_years:
            print(f"DEBUG: Fetching APEDA data for {fin_year}...")
            df = self.data_gov.fetch_apeda_data(fin_year, category, product_code)
            print(f"DEBUG: Received {len(df)} records from APEDA API")
            if len(df) > 0:
                all_data.append(df)
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Filter by states if specified
            if params.get('states') and 'State' in combined_df.columns:
                states_lower = [s.lower() for s in params['states']]
                combined_df = combined_df[combined_df['State'].str.lower().isin(states_lower)]
            
            results.append({
                'type': 'apeda_production',
                'data': combined_df.to_dict('records'),
                'years_used': fin_years
            })
            
            sources.append({
                'dataset': 'APEDA Production Statistics',
                'source': 'APEDA - Ministry of Commerce',
                'url': 'https://agriexchange.apeda.gov.in/'
            })
        
        return results, sources
    
    def query_daily_rainfall(self, params: dict) -> Tuple[List[Dict], List[Dict]]:
        """Query daily district-wise rainfall (2019-2024)"""
        results = []
        sources = []
        
        states = params.get('states', [])
        districts = params.get('districts', [])
        years = params.get('years', [])
        
        all_data = []
        for state in (states or [None]):
            for district in (districts or [None]):
                for year in (years or [None]):
                    df = self.data_gov.fetch_daily_rainfall(state, district, year, limit=100)
                    if len(df) > 0:
                        all_data.append(df)
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Calculate statistics if aggregation requested
            if params.get('aggregation') == 'average' and 'Avg_rainfall' in combined_df.columns:
                if 'State' in combined_df.columns:
                    avg_data = combined_df.groupby('State')['Avg_rainfall'].agg(['mean', 'sum', 'count']).reset_index()
                    avg_data.columns = ['State', 'Average_Daily_Rainfall_mm', 'Total_Rainfall_mm', 'Days']
                    
                    results.append({
                        'type': 'daily_rainfall_summary',
                        'data': avg_data.to_dict('records'),
                        'years_used': years
                    })
                else:
                    results.append({
                        'type': 'daily_rainfall',
                        'data': combined_df.to_dict('records')[:100],
                        'years_used': years
                    })
            else:
                results.append({
                    'type': 'daily_rainfall',
                    'data': combined_df.to_dict('records')[:100],
                    'years_used': years
                })
            
            sources.append({
                'dataset': 'Daily District-wise Rainfall Data',
                'source': 'data.gov.in - National Water Informatics Centre',
                'url': 'https://www.data.gov.in/'
            })
        
        return results, sources
    
    def query_historical_rainfall(self, params: dict) -> Tuple[List[Dict], List[Dict]]:
        """Query historical state-wise rainfall (1901-2015)"""
        results = []
        sources = []
        
        # Map state names to meteorological subdivisions
        subdivision_map = {
            'punjab': 'PUNJAB',
            'haryana': 'HARYANA DELHI & CHANDIGARH',
            'delhi': 'HARYANA DELHI & CHANDIGARH',
            'uttar pradesh': 'EAST UTTAR PRADESH',
            'maharashtra': 'MADHYA MAHARASHTRA',
            'karnataka': 'COASTAL KARNATAKA',
            'west bengal': 'GANGETIC WEST BENGAL',
            'tamil nadu': 'TAMIL NADU & PUDUCHERRY',
            'kerala': 'KERALA',
            'rajasthan': 'WEST RAJASTHAN',
            'gujarat': 'GUJARAT REGION',
            'bihar': 'BIHAR',
            'odisha': 'ODISHA',
            'andhra pradesh': 'COASTAL ANDHRA PRADESH'
        }
        
        states = params.get('states', [])
        years = params.get('years', [])
        
        all_data = []
        for state in states:
            subdivision = subdivision_map.get(state.lower(), state.upper())
            
            # Fetch data
            if years:
                for year in years:
                    df = self.data_gov.fetch_historical_rainfall(subdivision, year, limit=100)
                    if len(df) > 0:
                        all_data.append(df)
            else:
                df = self.data_gov.fetch_historical_rainfall(subdivision, limit=100)
                if len(df) > 0:
                    all_data.append(df)
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Filter by years if specified
            if years and 'year' in combined_df.columns:
                year_ints = [int(y) if isinstance(y, str) and y.isdigit() else y for y in years if str(y).isdigit()]
                if year_ints:
                    combined_df = combined_df[combined_df['year'].isin(year_ints)]
            
            # Calculate statistics if needed
            if params.get('aggregation') == 'average' and 'annual' in combined_df.columns:
                if 'subdivision' in combined_df.columns:
                    avg_data = combined_df.groupby('subdivision').agg({
                        'annual': 'mean',
                        'jun_sep': 'mean'  # Monsoon season
                    }).reset_index()
                    avg_data.columns = ['Subdivision', 'Average_Annual_Rainfall_mm', 'Average_Monsoon_Rainfall_mm']
                    
                    results.append({
                        'type': 'historical_rainfall_average',
                        'data': avg_data.to_dict('records'),
                        'years_used': years or list(range(1901, 2016))
                    })
                else:
                    results.append({
                        'type': 'historical_rainfall',
                        'data': combined_df.to_dict('records')[:100],
                        'years_used': years
                    })
            else:
                results.append({
                    'type': 'historical_rainfall',
                    'data': combined_df.to_dict('records')[:100],
                    'years_used': years
                })
            
            sources.append({
                'dataset': 'Historical Rainfall Data (1901-2015)',
                'source': 'data.gov.in - India Meteorological Department (IMD)',
                'url': 'https://www.data.gov.in/'
            })
        
        return results, sources
    
    # Helper methods
    def _process_year_filters(self, years: list, df: pd.DataFrame) -> list:
        """Process year filters including 'last N years' logic"""
        year_filters = []
        for y in years:
            if isinstance(y, int):
                year_filters.append(str(y))
            elif isinstance(y, str):
                if y.isdigit():
                    year_filters.append(y)
                elif 'last' in y.lower():
                    import re
                    from datetime import datetime
                    match = re.search(r'(\d+)', y)
                    if match:
                        n = int(match.group(1))
                        current_year = datetime.now().year
                        requested_years = list(range(current_year - n + 1, current_year + 1))
                        
                        available_years = df['Crop_Year'].str.split('-').str[0].unique()
                        available_years = sorted([int(yr) for yr in available_years if yr.isdigit()])
                        
                        matching_years = [yr for yr in requested_years if yr in available_years]
                        if matching_years:
                            year_filters.extend([str(yr) for yr in matching_years])
                        else:
                            fallback_years = available_years[-n:] if len(available_years) >= n else available_years
                            year_filters.extend([str(yr) for yr in fallback_years])
        return year_filters
    
    def _convert_years_to_int(self, years: list, df: pd.DataFrame, year_column: str) -> list:
        """Convert year filters to integers"""
        year_ints = []
        for y in years:
            if isinstance(y, int):
                year_ints.append(y)
            elif isinstance(y, str) and y.isdigit():
                year_ints.append(int(y))
        return year_ints
    
    def _convert_to_financial_years(self, years: list) -> list:
        """Convert years to financial year format (YYYY-YY)"""
        fin_years = []
        for year in years:
            if isinstance(year, int):
                fin_years.append(f"{year}-{str(year+1)[-2:]}")
            elif isinstance(year, str) and '-' in year:
                fin_years.append(year)
            elif isinstance(year, str) and year.isdigit():
                y = int(year)
                fin_years.append(f"{y}-{str(y+1)[-2:]}")
        return fin_years
