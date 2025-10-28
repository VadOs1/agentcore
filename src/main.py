import os

from dotenv import load_dotenv

from openai import OpenAI
from src.open_ai.open_ai_vector_store import create_vector_store

if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    vector_store_name = 'The Dragons Reckoning Vector Store'
    vector_store_id = create_vector_store(client, vector_store_name)
