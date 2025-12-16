# app.py (or api.py)
from flask import Flask, jsonify, request
from flask_cors import CORS # Important for allowing your React app to fetch data
from google.cloud import bigquery
import pandas as pd
import os

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, or specify origins if needed

project_id = "ccibt-hack25ww7-733" # Your Google Cloud Project ID

def get_borrower_data(limit=100):
    """Fetches data from the Borrower table in BigQuery."""
    client = bigquery.Client(project=project_id)
    query = f"""
        SELECT *
        FROM `ccibt-hack25ww7-733.hackacthon_case2.BORROWER`
        LIMIT {limit}
    """
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df.to_dict(orient='records')

@app.route('/api/borrowers', methods=['GET'])
def borrowers():
    """API endpoint to get borrower data."""
    limit = request.args.get('limit', default=100, type=int)
    data = get_borrower_data(limit=limit)
    return jsonify(data)

@app.route('/')
def hello_world():
    return "Hello from your BigQuery API!"

if __name__ == '__main__':
    # When running in Cloud Shell, use host 0.0.0.0 for external access
    # and a port that Cloud Shell exposes (e.g., 8080)
    app.run(debug=True, host='0.0.0.0', port=8080)
