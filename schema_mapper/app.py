# app.py (or api.py)
from flask import Flask, jsonify, request
from flask_cors import CORS # Important for allowing your React app to fetch data
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, or specify origins if needed

# It's best practice to let the client library discover the project ID from the environment.
# The client will automatically use the project configured in your gcloud CLI or environment variables.
try:
    bq_client = bigquery.Client()
    print(f"Successfully connected to BigQuery project: {bq_client.project}")
except Exception as e:
    print(f"Could not initialize BigQuery client: {e}")
    bq_client = None

@app.route('/api/compare-tables', methods=['POST'])
def compare_table_counts():
    """
    Compares the row counts of a source and a target BigQuery table.
    Expects a JSON body with 'source_table' and 'target_table'.
    Example: {
        "source_table": "your-project.your_dataset.table1",
        "target_table": "your-project.your_dataset.table2"
    }
    """
    if not bq_client:
        return jsonify({"error": "BigQuery client is not initialized. Check server logs."}), 500

    req_data = request.get_json()
    if not req_data or 'source_table' not in req_data or 'target_table' not in req_data:
        return jsonify({"error": "Missing 'source_table' or 'target_table' in request body"}), 400

    source_table_id = req_data['source_table']
    target_table_id = req_data['target_table']

    try:
        # Fetch table metadata. This validates existence and gets the row count efficiently.
        source_table_obj = bq_client.get_table(source_table_id)
        target_table_obj = bq_client.get_table(target_table_id)

        source_count = source_table_obj.num_rows
        target_count = target_table_obj.num_rows

        if source_count == target_count:
            status = "matched"
            message = f"Row counts are identical."
        else:
            status = "not matched"
            comparison = "less than" if source_count < target_count else "greater than"
            message = f"Source table count is {comparison} target table count."

        return jsonify({
            "sourceTable": source_count,
            "targetTable": target_count,
            "status": status,
            "message": message
        })
    except NotFound as e:
        return jsonify({"error": f"Table not found: {e.message}"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/')
def hello_world():
    return "Hello from your BigQuery API!"

if __name__ == '__main__':
    # When running in Cloud Shell, use host 0.0.0.0 for external access
    app.run(debug=True, host='0.0.0.0', port=8080)
