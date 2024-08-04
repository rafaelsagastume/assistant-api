import io

from core.api import client_ai


async def create_vector_store(slug: str):
    # create vector store
    vector_store = await client_ai.beta.vector_stores.create(name=f"vector_store_{slug}")
    return vector_store


async def get_vector_store(slug: str):
    # get vector store
    vector_store = await client_ai.beta.vector_stores.retrieve(name=f"vector_store_{slug}")
    return vector_store


async def create_file(file_name: str, file: io.BytesIO, vector_store_id: str):
    # create file
    file = await client_ai.beta.vector_stores.files.upload(vector_store_id=vector_store_id, file=(file_name, file))
    return file


async def delete_file(file_id: str, vector_store_id: str):
    # delete file
    await client_ai.beta.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file_id)
    return True
