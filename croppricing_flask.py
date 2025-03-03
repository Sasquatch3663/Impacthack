from flask import Flask, request, jsonify
import requests

# SerpAPI key (Replace with your actual API key)
API_KEY = "12a0690a23d8d09af0c65223f0da3def0791295378c4e7897c0cfe5d6ba1bda2"

app = Flask(__name__)

# Function to fetch crop price
def fetch_crop_price(crop_name, state):
    params = {
        "engine": "google",
        "q": f"{crop_name} price per kg in {state}, India",
        "api_key": API_KEY,
    }
    
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    
    # Extract relevant data (Parsing might depend on search results structure)
    for result in data.get("organic_results", []):
        snippet = result.get("snippet", "")
        if "₹" in snippet:
            return {
                "title": result.get("title", "No title found"),
                "details": snippet
            }  # Return complete detail
    
    return {"error": "No data found"}

@app.route('/fetch_price', methods=['GET'])
def get_price():
    crop_name = request.args.get('crop_name')
    state = request.args.get('state')
    
    if not crop_name or not state:
        return jsonify({"error": "Please provide both crop_name and state"}), 400
    
    price_data = fetch_crop_price(crop_name, state)
    return jsonify(price_data)

if __name__ == '__main__':
    app.run(debug=True)
