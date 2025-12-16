from google.adk.agents.llm_agent import Agent
import workers.storage_agent as storage_agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='An agent that performs intelligent schema discovery, data conversion, and bigquery data loading',
    instruction='''You are an orchestrator. 
    Delegate all Cloud Storage and file-browsing tasks to the storage_specialist.
    When asked what you can do, explain that you manage a team of specialists including a storage expert.''',
    sub_agents=[storage_agent.storage_specialist]
)
