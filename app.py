from flask import Flask, jsonify, request, make_response
import openai
import logging
import sys

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
            api_key = request.form.get('api_key')
            if not name or not api_key:
                error_message = "Company name and API key are required."
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
                    <h2>Company GPT Info</h2>
                    <form method="post">
                        <input type="text" name="name" placeholder="Enter company name" required>
                        <br>
                        <input type="text" name="api_key" placeholder="Enter your OpenAI API key" required>
                        <br>
                        <input type="submit" value="Ask GPT">
                    </form>
                    {result_html}
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

