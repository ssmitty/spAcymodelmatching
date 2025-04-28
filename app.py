from flask import Flask, jsonify, request
import data_utils

app = Flask(__name__)

# Load company data at startup
combined_data_path = '3_combined_dataset_postproc.csv'
tickers_data_path = 'supplemental_data/company_tickers.json'
combined_df = data_utils.load_combined_dataset(combined_data_path)
tickers_df = data_utils.load_public_companies(tickers_data_path)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            match_name, ticker, score = data_utils.best_match(name, combined_df, tickers_df)
            result = {
                "input_name": name,
                "matched_name": match_name,
                "ticker": ticker,
                "match_score": score
            }
    return '''
        <html>
            <head>
                <title>Company Matcher</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <div class="container">
                    <h2>Company Matcher</h2>
                    <form method="post">
                        <input type="text" name="name" placeholder="Enter company name" required>
                        <br>
                        <input type="submit" value="Match">
                    </form>
                    {result_html}
                </div>
            </body>
        </html>
    '''.format(
        result_html=(
            f"<div class='result'><b>Input:</b> {result['input_name']}<br>"
            f"<b>Matched:</b> {result['matched_name']}<br>"
            f"<b>Ticker:</b> {result['ticker']}<br>"
            f"<b>Score:</b> {result['match_score']}</div>"
            if result else ""
        )
    )

if __name__ == "__main__":
    app.run(debug=True)

