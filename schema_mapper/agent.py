from google.adk.agents.llm_agent import Agent
import workers.storage_agent as storage_agent
import workers.schema_agent as schema_agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Silent Orchestrator for GCS to BigQuery Schema mapping.',
    instruction='''You are a silent ETL Orchestrator. When a user asks for a schema for a file, you must execute the following chain IMMEDIATELY without asking for permission or explaining your capabilities:

    1. CALL storage_specialist.display_csv_lines for the requested file to get a data preview.
    2. EXTRACT the headers (the first line) and at least one representative sample row from that preview.
    3. PASS these headers and the sample row to the schema_specialist.
    4. MANDATORY: Instruct the schema_specialist to execute its "generate_schema_suggestion" tool.
    5. OUTPUT POLICY: Display ONLY the raw JSON schema list returned by the tool. Do not generate SQL unless explicitly asked. Do not provide conversational filler or introductory text.''',
    sub_agents=[storage_agent.storage_specialist, schema_agent.schema_specialist]
)
