from google.cloud import bigquery
import functions_framework
import json

# Initialize the BigQuery Client once globally
# It automatically handles authentication using the Function's Service Account
client = bigquery.Client()

@functions_framework.http
def execute_bigquery_sql(request):
    """
    Executes a one-off BigQuery SQL statement provided in the request body.
    """
    try:
        # 1. Parse the request body to get the SQL statement
        request_json = request.get_json(silent=True)
        if not request_json or 'sql_statement' not in request_json:
            return 'Error: No SQL statement found in request body.', 400

        sql_statement = request_json['sql_statement']

        # 2. Configure and run the query job
        # We use client.query_and_wait() to block until the job is complete,
        # which is ideal for one-off execution.
        query_job = client.query(sql_statement)  # Make the API request
        
        # Wait for the job to complete and get the results
        query_job.result() 

        # 3. Success response
        # You can add logic here to return query results if it was a SELECT statement.
        return f"BigQuery job {query_job.job_id} executed successfully. Status: {query_job.state}", 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error executing BigQuery SQL: {e}", 500