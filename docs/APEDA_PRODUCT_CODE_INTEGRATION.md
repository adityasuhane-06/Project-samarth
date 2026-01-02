# APEDA Data Integration

## Overview

APEDA (Agricultural and Processed Food Products Export Development Authority) provides state-level agricultural production data from 2019-2024.

**Source**: agriexchange.apeda.gov.in - Ministry of Commerce  
**Coverage**: 2019-2024 (Financial Years)  
**Granularity**: State-level aggregated data  
**Categories**: Agri, Fruits, Vegetables, Spices, LiveStock, Plantations, Floriculture

---

## Implementation

### Automatic Product Code Resolution

The system automatically maps crop names to APEDA product codes:

```python
# User query: "rice production in Punjab 2023-24"
# System automatically:
# 1. Identifies crop: "rice"
# 2. Finds product code: "1011"
# 3. Fetches data for rice specifically
```

### Key Methods

**`src/services/data_integration.py`**

```python
def find_product_code(self, crop_name: str) -> Optional[str]:
    """Find product code for a crop using fuzzy matching"""
    # Supports aliases: paddy→rice, corn→maize, chana→gram
    
def fetch_apeda_data(self, fin_year, category, product_code, report_type):
    """Fetch production data from APEDA API"""
```

**`src/services/langgraph_agent.py`**

```python
@tool
def fetch_apeda_production(state, year, commodity, category):
    """LangGraph tool that auto-resolves product codes"""
```

---

## Usage Examples

### Query 1: State-specific crop production
```
"rice production in Punjab 2023-24"
→ Product Code: 1011
→ Result: 14,356 thousand tonnes (10.42% of India)
```

### Query 2: Fruit production
```
"mango production in Maharashtra 2023-24"
→ Category: Fruits
→ Result: State-level mango production data
Product Code: 1013 (Wheat)
Result: 11,191 thousand tonnes (9.88% of India) ✅
```

### Test 3: Maharashtra Mango 2023-24
```
Query: "mango production in Maharashtra 2023-24"
Product Code: 1050 (Mango)
Result: 485.92 thousand tonnes (2.17% of India) ✅
```

### Test 4: Top Cotton States 2022-23
```
Query: "cotton production in India 2022-23"
Product Code: 1016 (Cotton)
Top 5 States:
  1. Gujarat: 8,795 thousand tonnes (26.13%)
  2. Maharashtra: 8,316 thousand tonnes (24.71%)
  3. Telangana: 5,745 thousand tonnes (17.07%)
  4. Rajasthan: 2,774 thousand tonnes (8.24%)
  5. Karnataka: 2,568 thousand tonnes (7.63%) ✅
```

---

## Available Product Codes (113 total)

### Agriculture (Agri) - 17 products
1001=Tobacco, 1002=Bajra, 1003=Cereals, 1004=Jowar, 1005=Sunflower, 1006=Gram, 1007=Groundnut, 1008=Lentil (Masur), **1009=Maize**, 1010=Pulses, **1011=Rice**, 1012=Tur (Arhar), **1013=Wheat**, 1014=Soyabean, 1015=Sugarcane, 1016=Cotton, 1017=Rapeseed & Mustard

### Fruits - 29 products
1038=Almond, 1039=Aonla/Gooseberry, 1040=Apple, 1041=Bael, 1042=Banana, 1043=Ber, 1044=Custard Apple, 1045=Grapes, 1046=Guava, 1047=Jack Fruit, 1048=Kiwi, 1049=Litchi, **1050=Mango**, 1051=Papaya, 1052=Passion Fruit, 1053=Peach, 1054=Pear, 1055=Picanut, 1056=Pineapple, 1057=Plum, 1058=Pomegranate, 1059=Sapota, 1060=Strawberry, 1061=Walnut, 1062=Other Fruits, 1063=Lime/Lemon, 1064=Mandarin, 1065=Sweet Orange, 1066=Other Citrus

### Vegetables - 25 products
1067=Beans, 1068=Bittergourd, 1069=Bottlegourd, 1070=Brinjal, 1071=Cabbage, 1072=Capsicum, 1073=Carrot, 1074=Cauliflower, 1075=Cucumber, 1076=Chillies (Green), 1077=Elephant Foot Yam, 1078=Muskmelon, 1079=Okra/Ladyfinger, **1080=Onion**, 1081=Parwal/Pointed Gourd, 1082=Peas, **1083=Potato**, 1084=Radish, 1085=Sitaphal/Pumpkin, 1086=Sweet Potato, 1087=Tapioca, **1088=Tomato**, 1089=Watermelon, 1090=Mushroom, 1091=Others Vegetables

### Spices - 17 products
1096=Pepper, 1097=Ginger, **1098=Chillies**, 1099=Turmeric, 1100=Garlic, 1101=Cardamom, 1102=Coriander, 1103=Cumin, 1104=Fennel, 1105=Fenugreek, 1106=Ajwan, 1107=Dill/Poppy/Celery, 1108=Cinnamon/Tejpat, 1109=Nutmeg, 1110=Clove, 1111=Tamarind, 1112=Saffron/Vanilla

### Plantations - 4 products
1092=Arecanut, 1093=Cashewnut, 1094=Cocoa, 1095=Coconut

### Floriculture - 11 products
1027=Anthurium, 1028=Carnation, 1029=Chrysanthemum, 1030=Gerbera, 1031=Gladiolus, 1032=Jasmine, 1033=Marigold, 1034=Orchids, 1035=Rose, 1036=Tube Rose, 1037=Tulip

### LiveStock - 10 products
1018=Buffalo Meat, 1019=Cattle Meat, 1020=Egg, 1021=Goat Meat, 1022=Meat, 1023=Milk, 1024=Poultry Meat, 1025=Sheep Meat, 1026=Swine Meat, 1113=Honey

---

## System Architecture

```
User Query: "rice production in Punjab 2023"
    ↓
LangGraph Agent
    ↓
fetch_apeda_production(state="Punjab", year="2023", commodity="rice")
    ↓
data_service.find_product_code("rice") → "1011"
    ↓
data_service.fetch_product_codes() [Cached after first call]
    ↓
APEDA API: POST GetIndiaProductionCatObject
    Body: {Category: "Agri", Financial_Year: "2023-24", product_code: "1011"}
    ↓
Filter by state: Punjab
    ↓
Return: {
    "source": "APEDA India",
    "commodity": "rice",
    "product_code": "1011",
    "data": [{"State": "Punjab", "Production": 14356.0, "Percent_Share": 10.42}],
    "note": "APEDA production data for rice in Punjab"
}
```

---

## Benefits

1. **Accurate Data**: Crop-specific production data instead of aggregates
2. **Automatic Matching**: No manual product code lookup required
3. **Fuzzy Matching**: Handles aliases (paddy→rice, corn→maize)
4. **Cached Product List**: Only fetches product codes once per session
5. **113 Products**: Covers all major crops, fruits, vegetables, spices, livestock
6. **Category Aware**: Automatically queries correct category (Agri, Fruits, etc.)
7. **Error Handling**: Falls back gracefully if product not found

---

## Next Steps

### 1. Update Render Deployment
```bash
# Set environment variables in Render dashboard:
SECRET_KEY=<your_gemini_api_key_1>
AGENT_API_KEY=<your_gemini_api_key_2>
API_GUESSING_MODELKEY=<your_gemini_api_key_3>
```

### 2. Test Production System
- Deploy code changes to GitHub
- Verify auto-deployment on Render
- Test queries:
  - "rice production in Punjab 2023"
  - "wheat in Haryana 2024"
  - "mango production in Maharashtra"

### 3. Documentation
- Update ARCHITECTURE.md with APEDA product code flow
- Add to TECHOLUTION_INTERVIEW.md
- Document in PROJECT_SUMMARY.md

---

## Interview Talking Points (Techolution)

### Problem
"The APEDA API required numeric product codes, but there was no documented way to get them. Manual lookup from network tab was impractical for an AI agent."

### Investigation
"I systematically tested endpoint patterns, analyzed page source, and discovered a hidden API endpoint that returns all product codes with their mappings."

### Solution
"Integrated automatic product code matching with fuzzy matching and alias support. Now the system accurately retrieves crop-specific data instead of aggregates."

### Impact
"Improved data accuracy from aggregate state-level totals (125k tonnes) to actual crop-specific production (14.4k tonnes rice) - a 10x difference that matters for decision-making."

### Technical Skills Demonstrated
- API reverse engineering
- Endpoint discovery through systematic testing
- Data integration patterns
- Caching strategies
- Error handling and fallbacks
- LangGraph tool design

---

## Files Modified
1. `src/services/data_integration.py` - Added product code fetching and matching
2. `src/services/langgraph_agent.py` - Updated APEDA tool with commodity parameter
3. `test/apeda_product_list.py` - Discovery script (kept for reference)
4. `test/verify_product_code_integration.py` - Verification tests

## Test Files Created
- `test/apeda.py` - Direct APEDA API testing
- `test/apeda_product_list.py` - Product list endpoint discovery
- `test/test_product_code_matching.py` - Matching logic tests
- `test/verify_product_code_integration.py` - End-to-end verification

---

**Status**: ✅ Complete and Verified
**Date**: December 29, 2024
**Next Action**: Deploy to production (Render)
