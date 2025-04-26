import pandas as pd
from fuzzy_matcher import FuzzyMatcher

def main():
    # Create a sample DataFrame with company names
    sample_companies = pd.DataFrame({
        'Name': [
            'Target',
            'Microsoft Corporation',
            'Apple Inc',
            'Some Random Company'  # This one shouldn't match
        ]
    })

    # Initialize the matcher
    matcher = FuzzyMatcher()

    # Process the companies
    # This will save to results.csv and return the DataFrame
    results = matcher.process_companies(
        sample_companies,
        save_path='results.csv'
    )

    # Print the results
    print("\nMatching Results:")
    print(results)

if __name__ == "__main__":
    main() 