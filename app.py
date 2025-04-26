from flask import Flask, jsonify, request
import data_utils

app = Flask(__name__)

# Load company data at startup
data_path = 'supplemental_data/company_tickers.json'
public_companies = data_utils.load_public_companies(data_path)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/match_company', methods=['POST'])
def match_company():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing company name"}), 400
    name = data['name']
    match, score = data_utils.best_match(name, public_companies)
    return jsonify({
        "input_name": name,
        "matched_name": match,
        "match_score": score
    })

@app.route('/match_companies', methods=['POST'])
def match_companies():
    data = request.get_json()
    if not data or 'companies' not in data:
        return jsonify({"error": "Missing companies list"}), 400
    results = []
    for company in data['companies']:
        if not isinstance(company, dict) or 'id' not in company or 'name' not in company:
            return jsonify({"error": "Invalid company format"}), 400
        match, score = data_utils.best_match(company['name'], public_companies)
        results.append({
            "id": company['id'],
            "input_name": company['name'],
            "matched_name": match,
            "match_score": score
        })
    return jsonify({
        "matches": results,
        "total_processed": len(results)
    })

@app.route('/update_data', methods=['POST'])
def update_data():
    global public_companies
    try:
        public_companies = data_utils.load_public_companies(data_path)
        return jsonify({"status": "reloaded"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 