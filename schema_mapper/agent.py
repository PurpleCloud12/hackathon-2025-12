from google.adk.agents.llm_agent import Agent
import workers.storage_agent as storage_agent
import workers.schema_agent as schema_agent
import tools.storage_tools as storage_tools
import tools.schema_tools as schema_tools

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='ETL Orchestrator capable of both conversational support and automated schema mapping.',
    instruction='''You are an ETL Orchestrator. 
    
    CRITICAL WORKFLOW for "Generate mapping for [filename]":
    1. GATHER DATA: Use retrieve_source_data and retrieve_target_schema to get the CSV preview and SQL DDL.
    2. CREATE CONTEXT: Call get_mapping_context with those results to generate the raw source/target JSON.
    3. TRANSFORM: Pass that raw JSON output to the schema_specialist. 
    4. MANDATE: Explicitly command the schema_specialist: "Flatten this data into a single JSON list with 4 keys: csv_column, sql_column, type, and mode. Remove the 'csv_source_fields' and 'target_sql_columns' wrappers."
    
    If any tool returns an error, stop and show the error. Otherwise, proceed until ONLY the final cleaned JSON is displayed. No conversational filler.''',
    tools=[
        storage_tools.retrieve_source_data,
        storage_tools.retrieve_target_schema,
        schema_tools.get_mapping_context
    ],
    sub_agents=[storage_agent.storage_specialist, schema_agent.schema_specialist]
)
