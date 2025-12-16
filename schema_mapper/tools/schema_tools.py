import re
import json

def infer_bigquery_type(sample_value: str) -> str:
    """Helper to determine a BigQuery type for a single string value."""
    if not sample_value or sample_value.lower() in ['null', 'nan', '']:
        return "STRING"
    if re.fullmatch(r'-?\d+', sample_value):
        return "INT64"
    if re.fullmatch(r'-?\d*\.\d+', sample_value):
        return "FLOAT64"
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', sample_value):
        return "DATE"
    return "STRING"

def generate_schema_suggestion(csv_headers: list[str], sample_row: list[str]) -> str:
    """
    Takes headers and a sample row to produce a starting BigQuery JSON schema.
    
    Args:
        csv_headers: List of column names.
        sample_row: List of values from a representative row.
    """
    schema = []
    for header, value in zip(csv_headers, sample_row):
        detected_type = infer_bigquery_type(str(value))
        schema.append({
            "name": header.replace(" ", "_").replace("-", "_"),
            "type": detected_type,
            "mode": "NULLABLE"
        })
    
    return json.dumps(schema, indent=2)
