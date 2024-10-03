from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/run-python', methods=['POST'])
def run_python_script():
    try:
        # Run the Python script
        result = subprocess.run(['python', 'ui.py'], capture_output=True, text=True)
        return jsonify({"output": result.stdout})  # Return the script's output
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message if any
    

if __name__ == '__main__':
    app.run(debug=True)
