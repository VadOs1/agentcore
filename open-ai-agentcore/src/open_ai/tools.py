from agents import WebSearchTool, FileSearchTool
from openai import OpenAI

from vector_store import get_vector_store_id_by_name


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
