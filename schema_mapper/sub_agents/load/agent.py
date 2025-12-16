from google.cloud import bigquery
import functions_framework
import json

from google.adk import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.adk.tools import google_search
from google.genai import types
from google.adk.tools.tool_context import ToolContext

from . import prompt


# Initialize the BigQuery Client once globally
# It automatically handles authentication using the Function's Service Account
client = bigquery.Client()

@functions_framework.http
def execute_bigquery_sql(sql_statement):
    """
    Executes a one-off BigQuery SQL statement provided in the request body.
    """
    try:
        # 1. Parse the request body to get the SQL statement
        # request_json = request.get_json(silent=True)
        # if not request_json or 'sql_statement' not in request_json:
        #     return 'Error: No SQL statement found in request body.', 400

        # sql_statement = request_json['sql_statement']

        # 2. Configure and run the query job
        # We use client.query_and_wait() to block until the job is complete,
        # which is ideal for one-off execution.
        query_job = client.query(sql_statement)  # Make the API request

        # Wait for the job to complete and get the results
        result = query_job.result() 
        print (f"sql job status: {result}")

        # 3. Success response
        # You can add logic here to return query results if it was a SELECT statement.
        return f"BigQuery job {query_job.job_id} executed successfully. Status: {query_job.state}", 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error executing BigQuery SQL: {e}", 500

def append_to_state(
    tool_context: ToolContext, field: str, response: str
) -> dict[str, str]:
    """Append new output to an existing state key.

    Args:
        field (str): a field name to append to
        response (str): a string to append to the field

    Returns:
        dict[str, str]: {"status": "success"}
    """
    existing_state = tool_context.state.get(field, [])
    tool_context.state[field] = existing_state + [response]
    return {"status": "success"}

def dynamic_prompt(context: ToolContext):
    return prompt.LOAD_PROMPT

def _render_reference(
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> LlmResponse:
    """Appends grounding references to the response."""
    del callback_context
    if (
        not llm_response.content or
        not llm_response.content.parts or
        not llm_response.grounding_metadata
    ):
        return llm_response
    references = []
    for chunk in llm_response.grounding_metadata.grounding_chunks or []:
        title, uri, text = '', '', ''
        if chunk.retrieved_context:
            title = chunk.retrieved_context.title
            uri = chunk.retrieved_context.uri
            text = chunk.retrieved_context.text
        elif chunk.web:
            title = chunk.web.title
            uri = chunk.web.uri
        parts = [s for s in (title, text) if s]
        if uri and parts:
            parts[0] = f'[{parts[0]}]({uri})'
        if parts:
            references.append('* ' + ': '.join(parts) + '\n')
    if references:
        reference_text = ''.join(['\n\nReference:\n\n'] + references)
        llm_response.content.parts.append(types.Part(text=reference_text))
    if all(part.text is not None for part in llm_response.content.parts):
        all_text = '\n'.join(part.text for part in llm_response.content.parts)
        llm_response.content.parts[0].text = all_text
        del llm_response.content.parts[1:]
    return llm_response

load_agent = Agent(
    model='gemini-2.5-flash',
    name='load_agent',
    instruction=prompt.LOAD_PROMPT,
    tools=[append_to_state, execute_bigquery_sql],
    after_model_callback=_render_reference,
)
