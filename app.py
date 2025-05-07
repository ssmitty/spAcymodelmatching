from flask import Flask, jsonify, request, make_response
import openai
import logging
import sys
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

app = Flask(__name__)

API_VERSION = "0.1.0"

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error_message = None
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            api_key = os.environ.get('OPENAI_API_KEY')
            if not name:
                error_message = "Company name is required."
            elif not api_key:
                error_message = "OpenAI API key is not set in the backend."
            else:
                try:
                    client = openai.OpenAI(api_key=api_key)
                    prompt = (
                        f"Is '{name}' a public company listed on NASDAQ or NYSE? "
                        "If so, respond ONLY with the company name and its ticker symbol, separated by a colon (e.g., 'Apple Inc.: AAPL'). "
                        "If not, respond ONLY with '<COMPANY_NAME>: Not a public company'. Do not add any extra text."
                    )
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = response.choices[0].message.content.strip()
                except Exception as e:
                    logging.error(f"Error from OpenAI: {e}")
                    error_message = f"Error from OpenAI: {e}"
    except Exception as e:
        logging.error(f"Unexpected error in home route: {e}")
        error_message = "An unexpected error occurred. Please try again."

    result_html = ""
    if error_message:
        result_html = f"<div class='result' style='color:red;'><b>Error:</b> {error_message}</div>"
    elif result:
        result_html = f"<div class='result' style='word-break:break-word;max-width:500px;margin:auto;font-size:1.2em;padding:1em;background:#f9f9f9;border-radius:8px;border:1px solid #ddd;text-align:center;'><b>{result}</b></div>"

    html = f'''
        <html>
            <head>
                <title>Company GPT Info</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <div class="container">
                    <h2>Company Ticker Finder</h2>
                    <form method="post">
                        <input type="text" name="name" placeholder="Enter company name" required>
                        <br>
                        <input type="submit" value="Search Ticker">
                    </form>
                    <form action="/update_tickers" method="post" style="margin-top:20px;">
                        <button type="submit">Update Tickers</button>
                    </form>
                    {result_html}
                </div>
            </body>
        </html>
    '''
    response = make_response(html)
    response.headers["X-API-Version"] = API_VERSION
    return response

@app.route('/update_tickers', methods=['POST'])
def update_tickers():
    try:
        subprocess.run(['python3', 'update_tickers.py'], check=True)
        message = 'Tickers updated successfully.'
    except subprocess.CalledProcessError as e:
        message = f'Error updating tickers: {e}'
    html = f'''
        <html>
            <head>
                <title>Update Tickers</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <div class="container">
                    <h2>Update Tickers</h2>
                    <div class='result'>{message}</div>
                    <a href="/">Back to Home</a>
                </div>
            </body>
        </html>
    '''
    response = make_response(html)
    response.headers["X-API-Version"] = API_VERSION
    return response
# Optional: Add a global error handler for uncaught exceptions

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)

