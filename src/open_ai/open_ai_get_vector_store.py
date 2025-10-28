from openai import OpenAI


def get_vector_store_id_by_name(client: OpenAI, name: str, limit: int = 50) -> str:
    page = client.vector_stores.list(limit=limit)
    return next((vs.id for vs in page.data if vs.name == name), None)
