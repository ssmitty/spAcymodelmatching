# Company Matcher API

This project provides a Flask API and web interface to fuzzy match company names against a combined dataset and return the best match, including state, country, and ticker symbol (if the company is publicly traded).

## Features
- Fuzzy matching of company names using advanced preprocessing and token set ratio
- Ticker lookup using a merged NASDAQ and NYSE/AMEX dataset
- Returns company name, state, country, ticker, and match scores
- Batch processing utility for bulk matching
- Docker support for easy deployment

## Data Sources
- **Combined Dataset:** `3_combined_dataset_postproc.csv` (your main company database)
- **Tickers Dataset:** `supplemental_data/company_tickers.csv` (merged NASDAQ and NYSE/AMEX tickers, updated via script)

## Setup
1. **Clone the repository and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Update the tickers dataset (recommended before first run):**
   ```bash
   python update_tickers.py
   ```
   This script downloads and merges the latest NASDAQ and NYSE/AMEX tickers into `supplemental_data/company_tickers.csv`.

3. **Run the Flask app:**
   ```bash
   python app.py
   ```
   By default, the app runs on port 8080. If you see "Address already in use", either kill the process using that port or change the port in `app.py` (e.g., to 5000).

4. **Access the web interface:**
   - Go to [http://localhost:8080](http://localhost:8080) (or your chosen port)
   - Enter a company name to get the best match and ticker info

## API Usage
- The root endpoint `/` supports both GET (form) and POST (form submission).
- The API returns the matched company, ticker, state, country, and match scores.

## Batch Processing
You can process a batch of company names using the utility function in `data_utils.py`:
```python
from data_utils import process_and_save_batch, load_public_companies
import pandas as pd

batch_df = pd.read_csv('my_companies.csv')  # Must have a 'Name' column
public_companies = load_public_companies('supplemental_data/company_tickers.csv')
result_df = process_and_save_batch(batch_df, public_companies, save_path='results.csv')
```

## Troubleshooting
- **Port already in use:**
  - Find and kill the process using the port:
    ```bash
    lsof -i :8080
    kill <PID>
    ```
  - Or, change the port in `app.py` to a free port (e.g., 5000).
- **Ticker not found for public company:**
  - Make sure you have run `update_tickers.py` to get the latest tickers.
  - The fuzzy matching logic now uses advanced preprocessing and token set ratio for better accuracy.

## Notes
- The ticker dataset is now a CSV, not JSON.
- Fuzzy matching is robust to suffixes, punctuation, and word order.
- Only companies with a ticker match score >= 90 are assigned a ticker.

## License
MIT 