import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents import (
    FileSearchTool,
    InputGuardrailTripwireTriggered,
    WebSearchTool,
)
from agents import (
    Runner,
    Agent,
    ModelSettings,
)
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from dotenv import load_dotenv
from openai import OpenAI

from app.dragon_family_guard_rail import guardrail
from app.vector_store import create_vector_store, get_vector_store_id
from app.calculator_tool import calculator

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


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    vector_store_id = create_vector_store(client)
    data_agent = Agent(
        name="The Dragons Reckoning Agent",
        instructions=(
            f"{RECOMMENDED_PROMPT_PREFIX}\n"
            "You are The Dragon from The Dragon's Reckoning. Be precise and concise (≤3 sentences).\n"
            "Use file_search for questions about Dragons Reckoning, and web_search for current facts on the public web.\n"
            "If the user asks for arithmetic or numeric computation, HAND OFF to the Calculator agent."
        ),
        tools=[
            WebSearchTool(),
            FileSearchTool(
                vector_store_ids=[get_vector_store_id(client=client)],
                max_num_results=3,
            ),
        ],
        input_guardrails=[guardrail],
        handoffs=[calculator],
        model_settings=ModelSettings(temperature=0),
    )

    app.run()
