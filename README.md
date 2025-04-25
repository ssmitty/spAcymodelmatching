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

### 2. Match Multiple Companies
**Endpoint:** `/match_companies`
**Method:** POST
**Content-Type:** application/json

Request body:
```json
{
    "companies": [
        {"id": "1", "name": "First Company"},
        {"id": "2", "name": "Second Company"}
    ]
}
```

Response:
```json
{
    "matches": [
        {
            "id": "1",
            "input_name": "First Company",
            "matched_name": "Best Match First Company",
            "match_score": 95
        },
        {
            "id": "2",
            "input_name": "Second Company",
            "matched_name": "Best Match Second Company",
            "match_score": 93
        }
    ],
    "total_processed": 2
}
```

### 3. Health Check
**Endpoint:** `/health`
**Method:** GET

Response:
```json
{
    "status": "ok",
    "total_companies": 1000
}
```

## Notes

- The API uses fuzzy string matching with a threshold of 91% confidence
- Matches below this threshold return null for the matched_name
- The health endpoint can be used to verify if the company data is loaded correctly 