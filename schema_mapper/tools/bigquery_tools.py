from google.cloud import bigquery
import json
import os
import re

def load_csv_to_bigquery(mapping_json: str, csv_name: str) -> str:
    """
    Final step: Uses the JSON mapping to load the full CSV from GCS into BigQuery raw layer.
    """
    import json
    import re
    import os
    from google.cloud import bigquery

    # 1. Robust JSON Cleaning
    # This regex extracts the first [...] array it finds, ignoring markdown backticks or conversational text.
    match = re.search(r'\[\s*{.*}\s*\]', mapping_json, re.DOTALL)
    if not match:
        return "FAILED: Could not find a valid JSON array in mapping_json. Please ensure it is a list of objects."
    
    clean_json = match.group(0)

    try:
        mapping = json.loads(clean_json)
    except Exception as e:
        return f"FAILED: JSON Parsing Error. Error: {str(e)}. Received: {clean_json[:100]}..."

    # 2. Setup Clients and Paths
    client = bigquery.Client()
    bucket_name = os.environ.get("TARGET_GCS_BUCKET")
    # Clean slashes to prevent gs://bucket//file
    source_folder = os.environ.get("SOURCE_DATA_FOLDER", "").strip("/")
    dataset_id = os.environ.get("BQ_RAW_DATASET_ID", "")
    
    table_name = 'raw_' + csv_name.replace('.csv', '').split('/')[-1]
    table_id = f"{client.project}.{dataset_id}.{table_name}"

    # 3. Flexible Schema Building
    schema = []
    if not isinstance(mapping, list):
        return "FAILED: mapping_json must be a list of column definitions."

    for entry in mapping:
        if isinstance(entry, dict):
            # The agent is inconsistent; let's accept any of these name keys
            col_name = entry.get("sql_column") or entry.get("name") or entry.get("bigquery_column")
            col_type = entry.get("type", "STRING")
            col_mode = entry.get("mode", "NULLABLE")
            
            if col_name:
                schema.append(bigquery.SchemaField(
                    name=col_name,
                    field_type=col_type,
                    mode=col_mode
                ))

    if not schema:
        return "FAILED: The schema list is empty. Please ensure the JSON contains 'sql_column' and 'type' keys."

    # 4. Configure the Load Job
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    # 5. Safe URI Construction
    clean_csv_name = csv_name.lstrip("/")
    if source_folder:
        uri = f"gs://{bucket_name}/{source_folder}/{clean_csv_name}"
    else:
        uri = f"gs://{bucket_name}/{clean_csv_name}"
        
    print(f"DEBUG: Final URI = {uri}") 

    # 6. Execute
    try:
        load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
        load_job.result()  # Wait for completion
        return f"SUCCESS: Loaded {load_job.output_rows} rows into {table_id}."
    except Exception as e:
        return f"FAILED: BigQuery Load Error for {uri}: {str(e)}"
