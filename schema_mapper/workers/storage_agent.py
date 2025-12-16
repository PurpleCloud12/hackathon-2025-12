from google.adk.agents.llm_agent import Agent
from ..tools import storage_tools

storage_specialist = Agent(
    model='gemini-2.5-flash',
    name='storage_specialist',
    description='Specializes in browsing and reading files from Google Cloud Storage buckets.',
    instruction='''You are an expert at navigating GCS buckets. 
    Use list_source_data to see what files are available.
    Use list_target_schemas to view the available sql target schemas
    Use retrieve_source_data to inspect the contents of a specific file.
    Use retrieve_target_schema to retrieve the sql file for a particular CSV
    Report the file structure or file list back to the requester clearly.''',
    tools=[
        storage_tools.list_source_data,
        storage_tools.list_target_schemas,
        storage_tools.retrieve_source_data,
        storage_tools.retrieve_target_schema
    ] 
)


