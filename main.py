from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_URL = "https://api.izone.com.au/testsimplelocalcocb"

def send_request(payload):
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        # Attempt to parse JSON or handle simple text
        try:
            data = response.json()
        except ValueError:
            data = response.text  # Get response as text if not JSON
        return response.status_code, data
    else:
        return response.status_code, response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def status():
    payload = {
        "iZoneV2Request": {"Type": 1, "No": 0, "No1": 0}
    }
    status_code, data = send_request(payload)
    if status_code == 200:
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch status", "details": data}), status_code

@app.route('/control', methods=['POST'])
def control():
    command = request.get_json()
    if not command:
        return jsonify({"error": "No data provided"}), 400
    status_code, response_content = send_request(command)
    if status_code == 200:
        # Assuming response_content can be 'OK' or some JSON
        if response_content == 'OK':
            return jsonify({"status": "OK"}), 200
        else:
            return jsonify({"status": "success", "data": response_content}), 200
    else:
        # Handle plain text 'ERROR' or other error details
        if response_content == 'ERROR':
            return jsonify({"status": "ERROR"}), 400
        else:
            return jsonify({"error": "API error", "details": response_content}), 400

if __name__ == '__main__':
    app.run(debug=True)
