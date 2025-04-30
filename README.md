# Company Matching API

This Flask API provides endpoints to match company names against a database of public companies.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have the company tickers data file at `supplemental_data/company_tickers.json`

3. Run the API:
```bash
python app.py
```

The API will start on http://localhost:5000

## API Endpoints

### 1. Match Single Company
**Endpoint:** `/match_company`
**Method:** POST
**Content-Type:** application/json

Request body:
```json
{
    "name": "Company Name"
}
```

Response:
```json
{
    "input_name": "Company Name",
    "matched_name": "Best Match Company Name",
    "match_score": 95
}
```

```

## Notes

- The API uses fuzzy string matching with a threshold of 91% confidence
- Matches below this threshold return null for the matched_name
- The health endpoint can be used to verify if the company data is loaded correctly 