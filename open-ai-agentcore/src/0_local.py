import asyncio
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from agents import (
    Agent,
    FileSearchTool,
    ModelSettings,
    InputGuardrailTripwireTriggered,
    Runner,
    WebSearchTool,
)
from dotenv import load_dotenv
from openai import OpenAI

from app.open_ai_vector_store import create_vector_store, get_vector_store_id
from app.calculator_tool import calculator
from app.dragon_family_guard_rail import guardrail


async def main():
    try:
        await Runner.run(data_agent, "Tell me about Dragons children.")
        print("\n ERROR: guardrail did not work")
    except InputGuardrailTripwireTriggered as e:
        print(
            f"\n Guardrail expected:. is_blocked: {e.guardrail_result.output.output_info.get('is_blocked')}, "
            f"reasoning: {e.guardrail_result.output.output_info.get('reasoning')}"
        )

    out = await Runner.run(
        data_agent, "Summarize The Dragon's Reckoning in 2 sentences."
    )
    print(
        f"\n Allowed prompt output: {out.final_output}. Handled by agent: {out.last_agent.name}"
    )

    out = await Runner.run(data_agent, "Compute (12 + 22) / 2")
    print(
        f"\n (12 + 22) / 2 = {out.final_output}. Handled by agent: {out.last_agent.name}"
    )

    out = await Runner.run(
        data_agent,
        "Search the web for recent news about the James Webb Space Telescope and summarize briefly.",
    )
    print(f"\n Web_search: {out.final_output}. Handled by agent: {out.last_agent.name}")


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
    asyncio.run(main())
