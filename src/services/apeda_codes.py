"""
APEDA Product Code Mapping
Manually collected from https://agriexchange.apeda.gov.in/Production/IndiaCat

To find a product code:
1. Go to https://agriexchange.apeda.gov.in/Production/IndiaCat
2. Select product from dropdown
3. Open browser DevTools → Network tab
4. Submit the form
5. Look at the POST request payload for "product_code"
"""

# Product Code Mapping: {product_name: product_code}
APEDA_PRODUCT_CODES = {
    # Cereals & Grains
    "rice": "1011",
    "wheat": "1001",  # Need to verify
    "maize": "1005",  # Need to verify
    "bajra": "1008",  # Need to verify
    "jowar": "1004",  # Need to verify
    
    # Pulses
    "gram": "1006",  # Chickpeas/Chana
    "lentil": "1009",  # Masur
    "arhar": "1010",  # Tur/Pigeon Pea - Need to verify
    
    # Cash Crops
    "tobacco": "1001",
    "cotton": "1112",  # Need to verify
    "jute": "1053",  # Need to verify
    "sugarcane": "1212",  # Need to verify
    
    # Spices & Plantation
    "arecanut": "1092",
    "cardamom": "0906",  # Need to verify
    "pepper": "0904",  # Need to verify
    "turmeric": "0910",  # Need to verify
    
    # Nuts & Dry Fruits
    "almond": "1038",
    "cashew": "0801",  # Need to verify
    "walnut": "0802",  # Need to verify
    
    # Oilseeds
    "groundnut": "1202",  # Need to verify
    "sunflower": "1206",  # Need to verify
    "soybean": "1201",  # Need to verify
    "mustard": "1205",  # Need to verify
}

# Reverse mapping for quick lookup
APEDA_CODE_TO_PRODUCT = {v: k for k, v in APEDA_PRODUCT_CODES.items()}

def get_product_code(product_name):
    """
    Get APEDA product code for a given product name
    
    Args:
        product_name: Name of the agricultural product
    
    Returns:
        str: Product code if found, "All" otherwise
    """
    product_name_lower = product_name.lower().strip()
    return APEDA_PRODUCT_CODES.get(product_name_lower, "All")

def get_product_name(product_code):
    """
    Get product name for a given APEDA code
    
    Args:
        product_code: APEDA product code
    
    Returns:
        str: Product name if found, None otherwise
    """
    return APEDA_CODE_TO_PRODUCT.get(product_code)

if __name__ == "__main__":
    print("APEDA Product Code Mapping")
    print("="*80)
    print(f"\nTotal mapped products: {len(APEDA_PRODUCT_CODES)}")
    print("\nVerified mappings:")
    print("  - rice: 1011 ✓")
    print("  - gram: 1006 ✓")
    print("  - tobacco: 1001 ✓")
    print("  - arecanut: 1092 ✓")
    print("  - almond: 1038 ✓")
    print("\nNeed verification: wheat, maize, cotton, sugarcane, etc.")
    print("\nUsage:")
    print("  from apeda_codes import get_product_code")
    print("  code = get_product_code('rice')  # Returns '1011'")
