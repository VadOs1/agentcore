from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents import WebSearchTool, FileSearchTool
from openai import OpenAI
from vector_store import get_vector_store_id_by_name


main_agent_name = 'The Dragons Reckoning Agent'
main_agent_instructions = (f'{RECOMMENDED_PROMPT_PREFIX}\n'
                          'You are The Dragon from The Dragon\'s Reckoning. Be precise and concise (≤3 sentences).\n'
                          'Use file_search for questions about Dragons Reckoning, and web_search for current facts on the public web.\n'
                          'If the user asks for arithmetic or numeric computation, HAND OFF to the Calculator agent.')



def get_open_ai_tools(client: OpenAI, vector_store_name: str):
    return [
        WebSearchTool(),
        FileSearchTool(
            vector_store_ids=[
                get_vector_store_id_by_name(client=client, name=vector_store_name)
            ],
            max_num_results=3,
        ),
    ]
