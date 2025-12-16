import os
from types import SimpleNamespace
from google.cloud import storage

BUCKET_NAME = os.environ.get("TARGET_GCS_BUCKET", "")
FOLDER_PREFIX = os.environ.get("SOURCE_DATA_FOLDER", "")
TARGET_SCHEMA_PREFIX = os.environ.get("TARGET_SCHEMA_FOLDER", "")

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
def list_target_schemas() -> list[str]:
    """
    Lists all available SQL target schema files from the project's data storage.
    """
    if not BUCKET_NAME:
        return ["Error: TARGET_GCS_BUCKET environment variable is not set."]

    storage_client = storage.Client()
    
    prefix = TARGET_SCHEMA_PREFIX.lstrip("/")
    if prefix and not prefix.endswith("/"):
        prefix += "/"
        
    blobs = storage_client.list_blobs(BUCKET_NAME, prefix=prefix)
    
    sql_files = [
        blob.name.replace(prefix, "") 
        for blob in blobs 
        if blob.name.lower().endswith('.sql')
    ]
    
    if not sql_files:
        return [f"No SQL files found in {prefix}"]

    return sql_files

def retrieve_target_schema(csv_name: str) -> str:
    """
    Reads a corresponding sql file from the project's data storage based on the provided csv name.
    """
    if not BUCKET_NAME:
        return "Error: TARGET_GCS_BUCKET not set"

    schemas = list_target_schemas()
    
    search_name = csv_name.replace('.csv', '').lower()
    
    matched_files = [s for s in schemas if search_name in s.lower()]
    
    if not matched_files:
        return f"Error: No matching SQL schema found for '{search_name}' in {schemas}"
    
    target_sql_file = matched_files[0]
    
    namespace = validated_bucket(TARGET_SCHEMA_PREFIX, target_sql_file) 
    
    try:
        content = namespace.blob.download_as_text()
        return content 
    except Exception as e:
        return f"Error reading SQL file '{target_sql_file}': {str(e)}"

def retrieve_source_data(csv_name: str, lines: int = 10) -> str:
    """ Reads a given CSV file from the project's data storage and returns the first N lines.
    
    Args:
        csv_name: The name of the CSV file (e.g., 'borrowers.csv') to read.
        lines: How many lines to return (defaults to 10).
    """
    if not BUCKET_NAME:
        return "Error: TARGET_GCS_BUCKET not set."

    namespace = validated_bucket(FOLDER_PREFIX,csv_name) 
    if not namespace.blob.exists():
        return f"Error: File '{csv_name}' not found at path '{namespace.blob_path}'."

    try:
        content = namespace.blob.download_as_text()
        line_list = content.splitlines()
        
        preview = "\n".join(line_list[:int(lines)])
        return preview

    except Exception as e:
        return f"Error reading CSV: {str(e)}"

def validated_bucket(prefix: str, file_name: str) -> SimpleNamespace:
    """
    Validates the path and returns an object with 'name' and 'blob' attributes.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    
    clean_prefix = prefix.lstrip("/")
    if clean_prefix and not clean_prefix.endswith("/"):
        clean_prefix += "/"
    
    clean_filename = file_name.lstrip("/")
    blob_path = f"{clean_prefix}{clean_filename}"
    
    blob = bucket.blob(blob_path)

    return SimpleNamespace(
        name=clean_filename,
        blob=blob,
        path=blob_path
    )
