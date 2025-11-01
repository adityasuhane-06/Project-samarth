# Data.gov.in API Testing

This folder contains scripts to test and fetch real data from data.gov.in APIs.

## Files

- `test_datagov_api.py` - Main testing script for crop production data API
- API responses are saved as JSON files in this directory

## Getting Your API Key

1. Visit https://data.gov.in/
2. Create an account or login
3. Go to "My Account" section
4. Your API key will be displayed there
5. Copy the key and use it in the test scripts

## Running Tests

```powershell
# Activate virtual environment first
cd "C:\Users\Lenovo\Desktop\Project samarth"
.venv\Scripts\Activate.ps1

# Run the API tests
cd test\api_tests
python test_datagov_api.py
```

## API Information

### Crop Production API
- **Resource ID**: `35be999b-0208-4354-b557-f6ca9a5355de`
- **URL**: https://api.data.gov.in/resource/35be999b-0208-4354-b557-f6ca9a5355de
- **Documentation**: https://data.gov.in/resource/district-wise-season-wise-crop-production-statistics-1997

### Parameters
- `api-key` (required): Your API key
- `format`: json, xml, or csv (default: json)
- `limit`: Maximum number of records (default: 10, max depends on your key)
- `offset`: Skip N records for pagination
- `filters[field_name]`: Filter by field value

### Example Filters
```
filters[state_name]=Punjab
filters[crop]=Rice
filters[crop_year]=2022-23
filters[season]=Kharif
```

## Sample API Key

The script uses a sample key with 10 record limit:
`579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b`

**Note**: Get your own API key for unlimited access!

## Output Files

- `basic_test.json` - Basic API response (10 records)
- `large_test.json` - Larger dataset (50 records)
- `punjab_rice.json` - Filtered: Punjab Rice data
- `karnataka_groundnut.json` - Filtered: Karnataka Groundnut data

## Integrating with Main App

Once you test the API and verify it works, you can:

1. Update the API key in the main `.env` file:
   ```
   DATA_GOV_API_KEY=your_actual_api_key_here
   ```

2. The main app (`src/app.py`) will automatically use real data instead of sample data

3. Real-time data fetching will be enabled in production
