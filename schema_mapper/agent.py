from google.adk.agents.llm_agent import Agent
import workers.storage_agent as storage_agent
import workers.schema_agent as schema_agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Orchestrator for GCS data discovery and BigQuery schema generation.',
    instruction='''You are an ETL Orchestrator. Your job is to coordinate between the storage_specialist and the schema_specialist.
    
    FLOW:
    1. When a user asks for a schema, first ask the storage_specialist to "retrieve_source_data" for that specific file.
    2. Once you have the data, extract the headers (first line) and one sample row.
    3. Send those headers and the sample row to the schema_specialist.
    4. MANDATORY: Explicitly instruct the schema_specialist to use its "generate_schema_suggestion" tool and return the result as a raw JSON list.
    5. Do not generate SQL unless the user specifically asks for it; prioritize the JSON schema output from the tool.''',
    sub_agents=[storage_agent.storage_specialist, schema_agent.schema_specialist]
)
