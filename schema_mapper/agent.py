from google.adk.agents.llm_agent import Agent
import tools.storage_tools

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='An agent that performs intelligent schema discovery, data conversion, and bigquery data loading',
    instruction='''You are an agent that is skilled in schema discovery, data transformation, and extract-transform-load processes that load data into bigquery.
    When asked for what you can do list out all your tools''',
    tools=[tools.storage_tools.list_source_data,tools.storage_tools.display_csv_lines]
)
