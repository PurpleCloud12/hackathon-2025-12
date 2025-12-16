
from google.adk.agents import SequentialAgent

from .sub_agents.critic import critic_agent
from .sub_agents.reviser import reviser_agent


etl_transformer = SequentialAgent(
    name='ETL transformer',
    description=(
        'ETL transform agent which can generate BigQuery SQL for transforming the data from source tables to destination tables.'
    ),
    sub_agents=[],
)

root_agent = etl_transformer