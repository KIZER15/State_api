from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace with your Geoapify API key
API_KEY = "e7e865c48b804f76bbb06366d02ac4a9"

@app.route('/reverse-geocode', methods=['POST'])
def reverse_geocode():
    data = request.get_json()

    if not data or 'lat' not in data or 'lon' not in data:
        return jsonify({"error": "Latitude and longitude are required in JSON body"}), 400

    lat = data['lat']
    lon = data['lon']

    try:
        url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&apiKey={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['features'] and len(data['features']) > 0:
            properties = data['features'][0]['properties']
            state = properties.get('state')
            if state:
                return jsonify({"state": state})
            else:
                return jsonify({"error": "State not found"}), 404
        else:
            return jsonify({"error": "No results found"}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data from Geoapify API", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)