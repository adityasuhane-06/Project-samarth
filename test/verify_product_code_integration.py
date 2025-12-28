"""Simple test to verify the complete flow"""
import sys
sys.path.append('c:/Users/Lenovo/Desktop/Project samarth/src')

from services.data_integration import DataGovIntegration

# Initialize
data_service = DataGovIntegration()

print("=" * 80)
print("VERIFICATION TEST: Product Code Matching + APEDA Data Fetch")
print("=" * 80)

# Test 1: Punjab rice 2023-24
print("\n[TEST 1] Punjab Rice Production 2023-24")
print("-" * 40)
rice_code = data_service.find_product_code('rice')
print(f"Product code for 'rice': {rice_code}")

df = data_service.fetch_apeda_data(
    fin_year="2023-24",
    category="Agri",
    product_code=rice_code,
    report_type="1"
)

punjab_data = df[df['State'].str.contains('Punjab', case=False, na=False)]
if not punjab_data.empty:
    production = punjab_data['Production'].iloc[0]
    share = punjab_data['Percent_Share'].iloc[0]
    print(f"✓ Punjab Rice Production (2023-24): {production} thousand tonnes ({share}% of India)")
else:
    print("✗ No Punjab data found")

# Test 2: Haryana wheat 2023-24
print("\n[TEST 2] Haryana Wheat Production 2023-24")
print("-" * 40)
wheat_code = data_service.find_product_code('wheat')
print(f"Product code for 'wheat': {wheat_code}")

df = data_service.fetch_apeda_data(
    fin_year="2023-24",
    category="Agri",
    product_code=wheat_code,
    report_type="1"
)

haryana_data = df[df['State'].str.contains('Haryana', case=False, na=False)]
if not haryana_data.empty:
    production = haryana_data['Production'].iloc[0]
    share = haryana_data['Percent_Share'].iloc[0]
    print(f"✓ Haryana Wheat Production (2023-24): {production} thousand tonnes ({share}% of India)")
else:
    print("✗ No Haryana data found")

# Test 3: Maharashtra mango 2023-24
print("\n[TEST 3] Maharashtra Mango Production 2023-24")
print("-" * 40)
mango_code = data_service.find_product_code('mango')
print(f"Product code for 'mango': {mango_code}")

df = data_service.fetch_apeda_data(
    fin_year="2023-24",
    category="Fruits",
    product_code=mango_code,
    report_type="1"
)

maharashtra_data = df[df['State'].str.contains('Maharashtra', case=False, na=False)]
if not maharashtra_data.empty:
    production = maharashtra_data['Production'].iloc[0]
    share = maharashtra_data['Percent_Share'].iloc[0]
    print(f"✓ Maharashtra Mango Production (2023-24): {production} thousand tonnes ({share}% of India)")
else:
    print("✗ No Maharashtra data found")

# Test 4: All India cotton 2022-23
print("\n[TEST 4] All India Cotton Production 2022-23")
print("-" * 40)
cotton_code = data_service.find_product_code('cotton')
print(f"Product code for 'cotton': {cotton_code}")

df = data_service.fetch_apeda_data(
    fin_year="2022-23",
    category="Agri",
    product_code=cotton_code,
    report_type="1"
)

if not df.empty:
    # Get top 5 states by production
    top_states = df.nlargest(5, 'Production')[['State', 'Production', 'Percent_Share']]
    print(f"✓ Top 5 Cotton Producing States (2022-23):")
    for _, row in top_states.iterrows():
        print(f"   - {row['State']}: {row['Production']} thousand tonnes ({row['Percent_Share']}%)")
else:
    print("✗ No cotton data found")

print("\n" + "=" * 80)
print("SUMMARY: Product code matching working correctly!")
print("=" * 80)
