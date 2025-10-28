import os

from agents import (
    InputGuardrailTripwireTriggered,
)
from agents import (
    Runner, Agent, ModelSettings,
)
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from dotenv import load_dotenv
from openai import OpenAI

from open_ai.constants import vector_store_name, main_agent_name, main_agent_instructions
from open_ai.guard_rails import guardrail
from open_ai.open_ai_tools import get_open_ai_tools
from open_ai.open_ai_vector_store import create_vector_store
from open_ai.tools import calculator_agent

app = BedrockAgentCoreApp()


@app.entrypoint
async def invoke(payload):
    user_message = payload.get("prompt", "Hi")
    try:
        result = await Runner.run(data_agent, user_message)
        output = result.final_output
    except InputGuardrailTripwireTriggered:
        output = "I'd really rather not talk about anything about Dragon's Family."

    return {"result": output}


if __name__ == '__main__':
    load_dotenv()
    api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    vector_store_id = create_vector_store(client, vector_store_name)
    web_search, file_search = get_open_ai_tools(client, vector_store_name)
    data_agent = Agent(
        name=main_agent_name,
        instructions=main_agent_instructions,
        tools=[web_search, file_search],
        input_guardrails=[guardrail],
        handoffs=[calculator_agent],
        model_settings=ModelSettings(temperature=0),
    )

    app.run()
