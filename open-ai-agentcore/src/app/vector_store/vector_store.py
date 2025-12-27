from openai import OpenAI


def create_vector_store(client: OpenAI, vector_store_name: str):
    vector_store = client.vector_stores.create(name='The Dragons Reckoning Vector Store')

    uploaded_file = client.files.create(
        file=open('the_dragons_reckoning.txt', 'rb'),
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


def get_vector_store_id_by_name(client: OpenAI, name: str, limit: int = 50) -> str:
    page = client.vector_stores.list(limit=limit)
    return next((vs.id for vs in page.data if vs.name == name), None)
