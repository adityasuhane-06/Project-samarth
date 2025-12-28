"""Test the new product code matching functionality"""
import sys
sys.path.append('c:/Users/Lenovo/Desktop/Project samarth/src')

from services.data_integration import DataGovIntegration

# Initialize
data_service = DataGovIntegration()

# Test cases
test_crops = [
    'rice',
    'Rice',
    'RICE',
    'paddy',
    'Basmati',
    'wheat',
    'Wheat ',  # with trailing space like in API
    'maize',
    'corn',
    'cotton',
    'mango',
    'apple',
    'potato',
    'tomato',
    'chillies',
    'pepper',
    'onion',
    'some_unknown_crop'
]

print("=" * 80)
print("Testing Product Code Matching")
print("=" * 80)

for crop in test_crops:
    code = data_service.find_product_code(crop)
    if code:
        products = data_service.fetch_product_codes()
        info = products.get(code, {})
        print(f"✓ '{crop}' -> {code} ({info.get('name')}) [{info.get('category')}]")
    else:
        print(f"✗ '{crop}' -> NOT FOUND")

# Test fetching data with found product code
print("\n" + "=" * 80)
print("Testing APEDA Data Fetch with Product Code")
print("=" * 80)

rice_code = data_service.find_product_code('rice')
if rice_code:
    print(f"\nFetching Punjab rice data for 2023-24 using product_code={rice_code}...")
    df = data_service.fetch_apeda_data(
        fin_year="2023-24",
        category="Agri",
        product_code=rice_code,
        report_type="1"
    )
    
    if not df.empty:
        print(f"\n✓ Successfully fetched {len(df)} records")
        punjab_data = df[df['State'].str.contains('Punjab', case=False, na=False)]
        if not punjab_data.empty:
            print(f"\nPunjab Rice Production (2023-24):")
            print(punjab_data[['State', 'Production', 'Percent_Share']].to_string(index=False))
            print(f"\nProduction value: {punjab_data['Production'].iloc[0]} thousand tonnes")
        else:
            print("✗ No Punjab data found in response")
    else:
        print("✗ Empty DataFrame returned")
else:
    print("✗ Could not find product code for rice")
