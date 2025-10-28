import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
vector_store = client.vector_stores.create(name='The Dragons Reckoning Vector Store')

uploaded = client.files.create(
    file=open('./the_dragons_reckoning.txt', 'rb'),
    purpose='assistants',
)

vs_file = client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=uploaded.id,
)

print(vs_file.vector_store_id)
