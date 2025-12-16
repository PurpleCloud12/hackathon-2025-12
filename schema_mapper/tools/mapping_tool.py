import json
import logging

logger = logging.getLogger("mapping_tool")

def generate_mapping_data(csv_preview: str, target_ddl: str) -> str:
    """
    Analyzes CSV headers and SQL DDL to create a BigQuery mapping.
    The agent uses its own reasoning to generate this; this function 
    just acts as the 'Contract' for the agent to fill.
    """
    return f"CSV_DATA: {csv_preview} | SQL_DDL: {target_ddl}"
