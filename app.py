import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from generate_response import generate_response

# Load environment variables
load_dotenv()

print("Helklop")

app = Flask(__name__)

# Get Bearer token from environment
API_BEARER_TOKEN = os.getenv("API_BEARER_TOKEN")

@app.route('/')
def home():
    return "✅ API is running..."

print(f"[DEBUG] Loaded Bearer Token: {API_BEARER_TOKEN}")


@app.route('/answer', methods=['POST'])
def answer():
    try:
        # Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header missing or malformed"}), 401

        token = auth_header.split(" ")[1]
        if token != API_BEARER_TOKEN:
            return jsonify({"error": "Invalid Bearer token"}), 403

        # Get query
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Query required"}), 400

        # Generate answer
        response = generate_response(query)
        return jsonify({
            "query": query,
            "answer": response,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)