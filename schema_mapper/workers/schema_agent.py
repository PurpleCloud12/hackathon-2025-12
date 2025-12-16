from google.adk.agents.llm_agent import Agent
from tools.schema_tools import generate_schema_suggestion

schema_specialist = Agent(
    model='gemini-2.5-flash',
    name='schema_specialist',
    description='A specialist in data modeling and BigQuery schema design.',
    instruction='''You are a Senior Data Architect. 
    Your task is to take CSV previews and convert them into high-quality BigQuery schemas.
    
    1. Clean column names (use underscores, remove special characters).
    2. Use the generate_schema_suggestion tool to get a baseline.
    3. Use your intelligence to override the baseline if a column name implies a 
       specific type (e.g., 'is_active' should be BOOLEAN, even if the data is 0/1).
    4. Return a clean JSON schema or a CREATE TABLE statement as requested.''',
    tools=[generate_schema_suggestion]
)
