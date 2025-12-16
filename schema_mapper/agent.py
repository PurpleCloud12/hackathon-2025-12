from google.adk.agents.llm_agent import Agent
from google.adk.agents import SequentialAgent
from .tools import bigquery_tools
from .sub_agents.transform import transform_agent

from .workers import storage_agent
from .workers import schema_agent

from .tools import storage_tools
from .tools import schema_tools

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    instruction='''You are a Batch ETL Orchestrator. 

    When the user asks to "process all files" or "run the bulk load":
    1. DISCOVER: Call `list_csv_files` to get the list of targets.
    2. LOOP: For EACH file in that list:
        a. GATHER: Call `preview_source_data` and `retrieve_target_schema` (match the CSV name to the SQL filename).
        b. MAP: Use your internal reasoning to create the 4-key JSON mapping.
        c. LOAD: Call `load_csv_to_bigquery`.
    3. SUMMARY: After the loop, provide a report of which files succeeded and which failed.

    STRICT RULE: Do not ask for permission between files. Process the entire list once triggered.''',
    tools=[
        storage_tools.list_csv_files,
        storage_tools.preview_source_data,
        storage_tools.retrieve_target_schema,
        bigquery_tools.load_csv_to_bigquery
    ]
)
