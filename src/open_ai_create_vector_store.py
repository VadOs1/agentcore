import os

from dotenv import load_dotenv
from openai import OpenAI

from src.open_ai_get_vector_store import get_vector_store_id_by_name

load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
vector_store_name = 'The Dragons Reckoning Vector Store'
vector_store = client.vector_stores.create(name=vector_store_name)

uploaded_file = client.files.create(
    file=open('./the_dragons_reckoning.txt', 'rb'),
    purpose='assistants',
)

vs_file = client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=uploaded_file.id,
)

print(f'Vector store id created: {vs_file.vector_store_id}')
vector_store_id = get_vector_store_id_by_name(client, vector_store.name)
print(f'Vector store id retrieved: {vs_file.vector_store_id}')
