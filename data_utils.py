import pandas as pd
from fuzzywuzzy import process
import logging

def load_data(filepath):
    """Load a CSV file into a DataFrame."""
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        logging.error(f"Error loading data from {filepath}: {e}")
        raise

def load_public_companies(json_path):
    """Load public companies from a JSON file (transpose for correct orientation)."""
    try:
        return pd.read_json(json_path).transpose()
    except Exception as e:
        logging.error(f"Error loading public companies from {json_path}: {e}")
        raise

def load_combined_dataset(csv_path):
    """Load the combined dataset for name matching."""
    try:
        return pd.read_csv(csv_path)
    except Exception as e:
        logging.error(f"Error loading combined dataset from {csv_path}: {e}")
        raise

def best_match(name, combined_df, tickers_df):
    """Fuzzy match name in combined dataset, then get ticker from tickers dataset."""
    try:
        if not isinstance(name, str):
            return None, None, None, None, 0
        
        companies_list = combined_df['Name'].tolist()
        output = process.extractOne(name, companies_list)
        
        if output and len(output) == 2:
            matched_name, score = output
            if score < 91:
                return None, None, None, None, score
                
            matched_row = combined_df[combined_df['Name'] == matched_name]
            if matched_row.empty:
                return matched_name, None, None, None, score
            matched_row = matched_row.iloc[0]
            state = matched_row['State']
            country = matched_row['Country']
            
            ticker_titles = tickers_df['title'].tolist()
            ticker_output = process.extractOne(matched_name, ticker_titles)
            if ticker_output and len(ticker_output) == 2:
                ticker_match, ticker_score = ticker_output
                ticker_row = tickers_df[tickers_df['title'] == ticker_match]
                ticker = ticker_row['ticker'].values[0] if not ticker_row.empty else None
            else:
                ticker = None
                
            return matched_name, ticker, state, country, score
        else:
            return None, None, None, None, 0
    except Exception as e:
        logging.error(f"Error in best_match for name '{name}': {e}")
        return None, None, None, None, 0

def process_and_save_batch(batch_df, public_companies, save_path='results.csv'):
    """
    Process a DataFrame of companies, find matches, and append results to a CSV.
    """
    try:
        batch_df = batch_df.copy()
        batch_df['Match Results'] = batch_df['Name'].apply(lambda n: best_match(n, public_companies))
        batch_df['Ticker'] = batch_df['Match Results'].apply(lambda x: x[0])
        batch_df['Ticker Match Score'] = batch_df['Match Results'].apply(lambda x: x[1])
        batch_df.drop('Match Results', axis=1, inplace=True)
        mode = 'a' if pd.io.common.file_exists(save_path) else 'w'
        batch_df.to_csv(save_path, mode=mode, header=(not pd.io.common.file_exists(save_path)), index=False)
        return batch_df
    except Exception as e:
        logging.error(f"Error in process_and_save_batch: {e}")
        raise 