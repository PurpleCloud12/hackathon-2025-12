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

def parse_sql_ddl(sql_text: str) -> list[dict]:
    """Extracts column names, types, and modes, ignoring CREATE TABLE syntax."""
    pattern = re.compile(r'^\s+([a-zA-Z0-9_]+)\s+([A-Z0-9]+)(?:\s+(NOT NULL))?', re.MULTILINE | re.IGNORECASE)
    columns = []
    for match in pattern.finditer(sql_text):
        name, bq_type, not_null = match.groups()
        if name.upper() in ["CREATE", "TABLE", "PARTITION", "CLUSTER"]:
            continue
        columns.append({
            "name": name,
            "type": bq_type.upper(),
            "mode": "REQUIRED" if not_null else "NULLABLE"
        })
    return columns

def get_mapping_context(csv_preview: str, target_ddl: str) -> str:
    """
    Combines CSV discovery and SQL parsing into a structured context object.
    """
    lines = csv_preview.strip().split('\n')
    headers = [h.strip() for h in lines[0].split(',')]
    samples = [s.strip() for s in lines[1].split(',')] if len(lines) > 1 else [""] * len(headers)
    
    csv_discovery = []
    for h, s in zip(headers, samples):
        csv_discovery.append({"header": h, "inferred_type": infer_bigquery_type(s)})

    target_columns = parse_sql_ddl(target_ddl)

    return json.dumps({
        "csv_source_fields": csv_discovery,
        "target_sql_columns": target_columns
    }, indent=2)
