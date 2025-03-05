from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# SerpAPI key (Replace with your actual API key)
API_KEY = "30895d28ad8c06e61997f64a5b7a7c32f117e15dba79d4bed63662cb6a882f8c"

app = Flask(__name__)

CORS(app)
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
    return {"message" : "CORS is enabled"}
from waitress import serve

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
