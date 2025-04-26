import pandas as pd
from fuzzywuzzy import process

def load_data(filepath):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(filepath)

def load_public_companies(json_path):
    """Load public companies from a JSON file (transpose for correct orientation)."""
    return pd.read_json(json_path).transpose()

def best_match(name, public_companies):
    """Find the best match for a company name in the public_companies DataFrame."""
    if not isinstance(name, str):
        return None, 0
    companies_list = public_companies['title'].tolist()
    output = process.extractOne(name, companies_list)
    if output and len(output) == 2:
        match, score = output
        return (match if score > 91 else None, score)
    else:
        print(f"Unexpected output for name '{name}': {output}")
        return None, 0

def process_and_save_batch(batch_df, public_companies, save_path='results.csv'):
    """
    Process a DataFrame of companies, find matches, and append results to a CSV.
    """
    batch_df = batch_df.copy()
    batch_df['Match Results'] = batch_df['Name'].apply(lambda n: best_match(n, public_companies))
    batch_df['Ticker'] = batch_df['Match Results'].apply(lambda x: x[0])
    batch_df['Ticker Match Score'] = batch_df['Match Results'].apply(lambda x: x[1])
    batch_df.drop('Match Results', axis=1, inplace=True)
    mode = 'a' if pd.io.common.file_exists(save_path) else 'w'
    batch_df.to_csv(save_path, mode=mode, header=(not pd.io.common.file_exists(save_path)), index=False)
    return batch_df 