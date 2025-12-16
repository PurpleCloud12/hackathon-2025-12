import re
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mapping_context")

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
    logger.info("Parsing SQL DDL text...")
    
    # Regex pattern to match column definitions
    pattern = re.compile(r'^\s+([a-zA-Z0-9_]+)\s+([A-Z0-9]+)(?:\s+(NOT NULL))?', re.MULTILINE | re.IGNORECASE)
    columns = []
    
    matches = list(pattern.finditer(sql_text))
    if not matches:
        logger.warning("No column definitions found in the provided SQL DDL. Check your regex or DDL format.")
        
    for match in matches:
        name, bq_type, not_null = match.groups()
        if name.upper() in ["CREATE", "TABLE", "PARTITION", "CLUSTER"]:
            continue
            
        col_def = {
            "name": name,
            "type": bq_type.upper(),
            "mode": "REQUIRED" if not_null else "NULLABLE"
        }
        columns.append(col_def)
        logger.debug(f"Parsed SQL Column: {name} ({bq_type})")

    logger.info(f"Successfully parsed {len(columns)} columns from DDL.")
    return columns

def get_mapping_context(csv_preview: str, target_ddl: str) -> str:
    """
    Combines CSV discovery and SQL parsing into a structured context object.
    """
    logger.info("Generating mapping context from CSV preview and DDL.")
    
    try:
        lines = csv_preview.strip().split('\n')
        if not lines:
            raise ValueError("CSV preview is empty.")

        headers = [h.strip() for h in lines[0].split(',')]
        logger.info(f"Found {len(headers)} headers in CSV preview.")
        
        samples = [s.strip() for s in lines[1].split(',')] if len(lines) > 1 else [""] * len(headers)
        
        csv_discovery = []
        for h, s in zip(headers, samples):
            inferred = infer_bigquery_type(s)
            csv_discovery.append({"header": h, "inferred_type": inferred})
            logger.debug(f"CSV Header: {h} | Sample: {s} | Inferred: {inferred}")

        # Process SQL
        target_columns = parse_sql_ddl(target_ddl)

        context = {
            "csv_source_fields": csv_discovery,
            "target_sql_columns": target_columns
        }
        
        logger.info("Mapping context generated successfully.")
        return json.dumps(context, indent=2)

    except Exception as e:
        logger.exception("Error generating mapping context.")
        return json.dumps({"error": str(e)})
