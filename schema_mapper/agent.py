from google.adk.agents.llm_agent import Agent
from google.adk.agents import SequentialAgent

#from .workers.storage_agent import storage_agent
from .sub_agents.transform import transform_agent
from .sub_agents.load import load_agent

from .workers import storage_agent
from .workers import schema_agent

from .tools import storage_tools
from .tools import schema_tools

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='ETL Orchestrator capable of both conversational support and automated schema mapping.',
    instruction='''You are an ETL Orchestrator. 
    
    CRITICAL WORKFLOW for "Generate mapping for [filename]":
    1. GATHER DATA: Use retrieve_source_data and retrieve_target_schema to get the CSV preview and SQL DDL.
    2. CREATE CONTEXT: Call get_mapping_context with those results to generate the raw source/target JSON.
    3. TRANSFORM: Pass that raw JSON output to the transform agent. 
    4. LOAD: Pass the control to load_agent for loading the data in to destination tables in BigQuery
    5. MANDATE: Explicitly command the schema_specialist: "Flatten this data into a single JSON list with 4 keys: csv_column, sql_column, type, and mode. Remove the 'csv_source_fields' and 'target_sql_columns' wrappers."
    
    If any tool returns an error, stop and show the error. Otherwise, proceed until ONLY the final cleaned JSON is displayed. No conversational filler.''',
    tools=[
        storage_tools.retrieve_source_data,
        storage_tools.retrieve_target_schema,
        schema_tools.get_mapping_context
    ],
    sub_agents=[storage_agent.storage_specialist, schema_agent.schema_specialist, transform_agent, load_agent]
)
