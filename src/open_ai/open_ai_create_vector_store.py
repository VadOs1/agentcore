from openai import OpenAI

from src.open_ai.open_ai_get_vector_store import get_vector_store_id_by_name


def create_vector_store(client: OpenAI, vector_store_name: str):
    vector_store = client.vector_stores.create(name=vector_store_name)

    uploaded_file = client.files.create(
        file=open('open_ai/the_dragons_reckoning.txt', 'rb'),
        purpose='assistants',
    )

    vs_file = client.vector_stores.files.create(
        vector_store_id=vector_store.id,
        file_id=uploaded_file.id,
    )

    print(f'Vector store id created: {vs_file.vector_store_id}')
    vector_store_id = get_vector_store_id_by_name(client, vector_store_name)
    print(f'Vector store id retrieved: {vs_file.vector_store_id}')
    return vector_store_id
