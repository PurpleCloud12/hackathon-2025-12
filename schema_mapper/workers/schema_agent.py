from google.adk.agents.llm_agent import Agent
from ..tools.schema_tools import get_mapping_context

schema_specialist = Agent(
    model='gemini-2.5-flash',
    name='schema_specialist',
    instruction='''You are a Senior Data Architect. 
    You will receive a JSON object containing "csv_source_fields" and "target_sql_columns".
    
    YOUR ONLY TASK:
    Correlate the two and return a SINGLE JSON list. 
    Each object in your list MUST have: "csv_column", "sql_column", "type", and "mode".

    - Use the SQL name for "sql_column".
    - Use the SQL type for "type" (e.g., if CSV is FLOAT64 but SQL is NUMERIC, use NUMERIC).
    - If a CSV field has no logical match in the SQL, set "sql_column" to null.
    
    DO NOT return the 'csv_source_fields' or 'target_sql_columns' keys. 
    DO NOT provide introductory text.''',
    tools=[get_mapping_context]
)
