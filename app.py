from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

@app.route('/run-python', methods=['POST'])
def run_python_script():
    try:
        # Extract data from request
        data = request.get_json()
        
        print("Received data:", data)
        
        domains = data.get('domains')
        reportType = data.get('reportType')
        scanType = data.get('scanType')
        
        # Log the received data
        app.logger.info(f"Received data: {data}")

        # Convert the list of domains into a string argument
        domain_str = ','.join(domains)

        # Construct the command to run the Python script with arguments
        result = subprocess.run(
            ['python', 'UI.py', domain_str,reportType,scanType], 
            capture_output=True,
            text=True
        )

        # Log stdout and stderr for debugging
        app.logger.info(f"Script output: {result.stdout}")
        app.logger.error(f"Script error (if any): {result.stderr}")

        # Check if the subprocess executed successfully
        if result.returncode != 0:
            return jsonify({"error": "Script execution failed", "details": result.stderr}), 500

        # Assuming the output is printed as JSON, try to parse it
        try:
            scan_output = json.loads(result.stdout)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to decode JSON from script output", "output": result.stdout}), 500

        # Send back domains to the UI
        return jsonify({"domains": domains, "scan_output": scan_output})

    except Exception as e:
        app.logger.error(f"Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
