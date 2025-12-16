from google.adk.agents.llm_agent import Agent
from tools.schema_tools import get_mapping_context

schema_specialist = Agent(
    model='gemini-2.5-flash',
    name='schema_specialist',
instruction='''You are a JSON Generator. 
Output ONLY a MINIFIED JSON array on a SINGLE LINE.
NO whitespace, NO newlines, NO markdown backticks.
Example: [{"csv_column":"a","sql_column":"a","type":"STRING","mode":"NULLABLE"}]

If the mapping is long, do not add any explanation text, as it will cause a truncation error.''')
