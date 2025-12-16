from google.adk.agents.llm_agent import Agent
import tools.storage_tools

storage_specialist = Agent(
    model='gemini-2.5-flash',
    name='storage_specialist',
    description='Specializes in browsing and reading files from Google Cloud Storage buckets.',
    instruction='''You are an expert at navigating GCS buckets. 
    Use list_source_data to see what files are available.
    Use display_csv_lines to inspect the contents of a specific file.
    Report the file structure or file list back to the requester clearly.''',
    tools=[
        tools.storage_tools.list_source_data,
        tools.storage_tools.retrieve_source_data
    ]
)
