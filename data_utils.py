import pandas as pd
from fuzzywuzzy import process
import logging

def preprocess_name(name):
    """Remove common company suffixes and punctuation for better matching."""
    if not isinstance(name, str):
        return name
    name = name.lower().replace(',', '').replace('.', '').strip()
    suffixes = [
        ' inc', ' corporation', ' corp', ' ltd', ' llc', ' co',
        ' - common stock', '- common stock', ' common stock'
    ]
    for suffix in suffixes:
        if name.endswith(suffix):
            name = name[: -len(suffix)]
    return name.strip()

def load_data(filepath):
    """Load a CSV file into a DataFrame."""
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        logging.error(f"Error loading data from {filepath}: {e}")
        raise

def load_public_companies(csv_path):
    """Load public companies from a CSV file."""
    try:
        return pd.read_csv(csv_path)
    except Exception as e:
        logging.error(f"Error loading public companies from {csv_path}: {e}")
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
            logging.warning(f"Input name is not a string: {name}")
            return None, None, None, None, 0, None
        "If not a string it returns none"
        
        companies_list = combined_df['Name'].tolist()
        logging.info(f"Searching for: {name}")
        output = process.extractOne(name, companies_list)
        "Output holds the best match and the score"
        if output and len(output) == 2:
            matched_name, score = output
            logging.info(f"Best match: {matched_name} with score: {score}")
            "If the score is below 90 it returns none"
            if score <= 89:
                logging.info(f"Score {score} is below threshold of 90")
                return None, None, None, None, score, None
                
            matched_row = combined_df[combined_df['Name'] == matched_name]
            if matched_row.empty:
                logging.warning(f"Matched name {matched_name} not found in dataset")
                return matched_name, None, None, None, score, None
            "If the matched name is not found in the dataset it returns none"
            matched_row = matched_row.iloc[0]
            state = matched_row['State']
            country = matched_row['Country']
            logging.info(f"Found state: {state}, country: {country}")
            "It finds the state and country of the matched name"
            # Preprocess matched_name and ticker_titles for better matching
            pre_matched_name = preprocess_name(matched_name)
            ticker_titles = tickers_df['title'].tolist()
            pre_ticker_titles = [preprocess_name(t) for t in ticker_titles]
            # Debug: print all raw ticker titles containing 'Tesla'
            raw_tesla_titles = [t for t in ticker_titles if 'Tesla' in t or 'TESLA' in t or 'tesla' in t]
            logging.info(f"Raw ticker titles with 'Tesla': {raw_tesla_titles}")
            logging.info(f"Pre-matched name: '{pre_matched_name}'")
            for i, t in enumerate(pre_ticker_titles):
                if 'tesla' in t:
                    logging.info(f"Ticker title candidate {i}: '{t}'")
            ticker_output = process.extractOne(pre_matched_name, pre_ticker_titles)
            logging.info(f"Ticker output: {ticker_output}")
            "It finds the ticker of the matched name"
            if ticker_output and len(ticker_output) == 2:
                ticker_match, ticker_score = ticker_output
                logging.info(f"Found ticker match: {ticker_match} with score: {ticker_score}")
                if ticker_score >= 90:
                    # Find the original ticker row (not preprocessed)
                    idx = pre_ticker_titles.index(ticker_match)
                    ticker_row = tickers_df.iloc[[idx]]
                    ticker = ticker_row['ticker'].values[0] if not ticker_row.empty else None
                    logging.info(f"Ticker found: {ticker}")
                    return matched_name, ticker, state, country, score, ticker_score
                else:
                    logging.info(f"Ticker score {ticker_score} is below threshold of 91")
                    return matched_name, None, state, country, score, None
            else:
                logging.warning(f"No ticker match found for {matched_name}")
                return matched_name, None, state, country, score, None
            "If the ticker is not found it returns none"
        else:
            logging.warning(f"No match found for {name}")
            return None, None, None, None, 0, None
    except Exception as e:
        logging.error(f"Error in best_match for name '{name}': {e}")
        return None, None, None, None, 0, None

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