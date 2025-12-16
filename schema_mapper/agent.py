from google.adk.agents.llm_agent import Agent
from google.adk.agents import SequentialAgent

#from .workers.storage_agent import storage_agent
from .sub_agents.transform import transform_agent


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='An agent that performs intelligent schema discovery, data conversion, and bigquery data loading',
    instruction='''You are an orchestrator. 
    Delegate all Cloud Storage and file-browsing tasks to the storage_specialist.
    When asked what you can do, explain that you manage a team of specialists including a storage expert.''',
    #sub_agents=[storage_agent.storage_specialist]
    sub_agents = [transform_agent]
)
