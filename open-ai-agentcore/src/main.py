import asyncio
import os

from agents import (
    Agent,
    ModelSettings,
    InputGuardrailTripwireTriggered,
    Runner,
)
from dotenv import load_dotenv
from openai import OpenAI

from app.config import vector_store_name, main_agent_name, main_agent_instructions
from app.guard_rails import guardrail
from app.config import get_open_ai_tools
from app.vector_store import create_vector_store
from app.calculator_tull import calculator_agent


async def main():
    try:
        await Runner.run(data_agent, 'Tell me about Dragons children.')
        print('\n ERROR: guardrail did not work')
    except InputGuardrailTripwireTriggered as e:
        print(f'\n Guardrail expected:. is_blocked: {e.guardrail_result.output.output_info.get('is_blocked')}, '
              f'reasoning: {e.guardrail_result.output.output_info.get('reasoning')}')

    out = await Runner.run(data_agent, 'Summarize The Dragon\'s Reckoning in 2 sentences.')
    print(f'\n Allowed prompt output: {out.final_output}. Handled by agent: {out.last_agent.name}')

    out = await Runner.run(data_agent, "Compute (12 + 22) / 2")
    print(f'\n (12 + 22) / 2 = {out.final_output}. Handled by agent: {out.last_agent.name}')

    out = await Runner.run(data_agent,
                           'Search the web for recent news about the James Webb Space Telescope and summarize briefly.')
    print(f'\n Web_search: {out.final_output}. Handled by agent: {out.last_agent.name}')


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
    asyncio.run(main())
