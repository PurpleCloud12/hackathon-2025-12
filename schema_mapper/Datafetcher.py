from google.cloud import bigquery
import pandas as pd
import os

# Set your Google Cloud Project ID
# Cloud Shell usually has this environment variable set, but it's good practice
# to explicitly set it or ensure it's picked up.
# You can get your project ID from the Cloud Shell prompt or the Google Cloud console.
project_id = "ccibt-hack25ww7-733" # Your user's project ID

def get_borrower_data():
    """Fetches data from the Borrower table in BigQuery."""
    client = bigquery.Client(project=project_id)
    query = """
        SELECT *
        FROM `ccibt-hack25ww7-733.hackacthon_case2.BORROWER`
        LIMIT 1000  # Add a limit for development to avoid large data transfers
    """
    query_job = client.query(query)
    # Convert to DataFrame for easier handling
    df = query_job.to_dataframe()
    return df.to_dict(orient='records') # Return as list of dictionaries for JSON output

if __name__ == "__main__":
    # Example of how to call it and print data
    data = get_borrower_data()
    print(f"Fetched {len(data)} rows from Borrower table.")
    # For a quick check, print the first few rows
    if data:
        print(data[:5])
