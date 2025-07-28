from flask import Flask, jsonify
from core_logic import run_full_analysis # Import our main function

app = Flask(__name__)

@app.route("/analyze", methods=["GET"])
def analyze_instance():
    """API endpoint to trigger and return the instance analysis."""
    print("API endpoint '/analyze' was hit. Running analysis...")
    
    analysis_result = run_full_analysis()
    
    return jsonify(analysis_result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)