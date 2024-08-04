from fastapi import UploadFile

from core.manager.assistants import create_assistant, delete_assistant
from core.manager.files import create_file, create_vector_store
from src.assistants.models import (Assistant, AssistantFile,
                                   AssistantVectorStore)
from src.assistants.querys import (create_assistant_db, create_assistant_file,
                                   create_assistant_vector_store,
                                   delete_assistant_db, get_assistant_by_id,
                                   get_assistant_by_name,
                                   get_assistant_vector_store)


async def register_assistant(assistant: Assistant, organization: str):

    assistant_by_name = await get_assistant_by_name(assistant.name, organization)
    if assistant_by_name:
        raise Exception("Assistant already exists")

    try:
        assistant_data = await create_assistant(assistant.name, assistant.instructions, organization)

        assistant_class = Assistant(name=assistant.name, instructions=assistant.instructions,
                                    organization=organization, assistant_id=assistant_data.id)

        assistant_db = await create_assistant_db(assistant_class)
        return assistant_db
    except Exception as e:
        raise e


async def delete_assistant_by_id(id: str, organization: str):

    assistant_db = await get_assistant_by_id(id)
    if not assistant_db:
        raise Exception("Assistant not found")

    if assistant_db.organization != organization:
        raise Exception("You don't have permission to delete this assistant")

    try:
        await delete_assistant(assistant_db.assistant_id)
        await delete_assistant_db(id)
        return True
    except Exception as e:
        raise e


async def register_assistant_file(file: UploadFile, assistant_db_id: str, organization: str):

    assistant = await get_assistant_by_id(assistant_db_id)
    if not assistant:
        raise Exception("Assistant not found")

    file_name = file.filename
    allowed_extensions = ['txt', 'pdf', 'docx']
    extension = file.filename.split('.')[-1].lower()

    if extension not in allowed_extensions:
        raise Exception(
            f"Files with extensions [{extension}] are not supported, only [{', '.join(allowed_extensions)}] are supported")

    try:
        vector = await get_assistant_vector_store(assistant.assistant_id)
        if not vector:
            vector_db = await create_vector_store(assistant.slug)
            vector = AssistantVectorStore(
                vector_store_id=vector_db.id, assistant_id=assistant.assistant_id)
            await create_assistant_vector_store(vector)
        vector_id = vector.vector_store_id

        file = await create_file(file.filename, file.file, vector_id)
        assistant_file = AssistantFile(
            name=file_name, assistant_id=assistant_db_id, file_id=file.id, organization=organization)
        assistant_file_db = await create_assistant_file(assistant_file)
        return assistant_file_db
    except Exception as e:
        raise e
