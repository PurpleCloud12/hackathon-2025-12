import os
from google.cloud import storage

BUCKET_NAME = os.environ.get("TARGET_GCS_BUCKET", "")
FOLDER_PREFIX = os.environ.get("TARGET_FOLDER", "")

def list_source_data() -> list[str]:
    """
    Lists all available CSV source data files from the project's data storage.
    """
    if not BUCKET_NAME:
        return ["Error: TARGET_GCS_BUCKET environment variable is not set."]

    storage_client = storage.Client()
    
    prefix = FOLDER_PREFIX.lstrip("/")
    if prefix and not prefix.endswith("/"):
        prefix += "/"
        
    blobs = storage_client.list_blobs(BUCKET_NAME, prefix=prefix)
    
    csv_files = [
        blob.name.replace(prefix, "") 
        for blob in blobs 
        if blob.name.lower().endswith('.csv')
    ]
    
    if not csv_files:
        return [f"No CSV files found in {prefix}"]

    return csv_files
def retrieve_source_data(csv_name: str, lines: int = 10) -> str:
    """
    Reads a given CSV file from the project's data storage and returns the first N lines.
    
    Args:
        csv_name: The name of the CSV file (e.g., 'borrowers.csv') to read.
        lines: How many lines to return (defaults to 10).
    """
    if not BUCKET_NAME:
        return "Error: TARGET_GCS_BUCKET not set."

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    
    clean_prefix = FOLDER_PREFIX.lstrip("/")
    if clean_prefix and not clean_prefix.endswith("/"):
        clean_prefix += "/"
    
    clean_filename = csv_name.lstrip("/")
    
    blob_path = f"{clean_prefix}{clean_filename}"
    
    blob = bucket.blob(blob_path)

    if not blob.exists():
        return f"Error: File '{csv_name}' not found at path '{blob_path}'."

    try:
        content = blob.download_as_text()
        line_list = content.splitlines()
        
        preview = "\n".join(line_list[:int(lines)])
        return preview

    except Exception as e:
        return f"Error reading CSV: {str(e)}"
