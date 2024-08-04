from bson import ObjectId

from core.db import assitants, files
from src.assistants.models import Assistant, AssistantFile


async def get_assistant_db(assistant_id: str):
    assistant = await assitants.find_one({"assistant_id": assistant_id})
    if assistant:
        return Assistant(**assistant)
    return None


async def get_assistant_by_id(id: str):
    assistant = await assitants.find_one({"_id": ObjectId(id)})
    if assistant:
        return Assistant(**assistant)
    return None


async def get_assistant_by_name(name: str, organization: str):
    assistant = await assitants.find_one({"name": name, "organization": organization})
    if assistant:
        return Assistant(**assistant)
    return None


async def create_assistant_db(assistant: Assistant):

    existing_assistant = await get_assistant_db(assistant.assistant_id)
    if existing_assistant:
        raise Exception("Assistant already exists")

    await assitants.insert_one(assistant.dict())

    assistant_db = await get_assistant_db(assistant.assistant_id)
    return assistant_db


async def get_list_assistants(organization: str):
    assistants = assitants.find({"organization": organization})

    items = []
    async for item in assistants:
        i = {
            "id": str(item["_id"]),
            "name": item["name"],
            "instructions": item["instructions"],
            "organization": item["organization"],
            "slug": item.get("slug", ""),
        }
        items.append(i)
    return items


async def delete_assistant_db(id: str):
    try:
        await assitants.delete_one({"_id": ObjectId(id)})
        return True
    except Exception as e:
        raise e


async def get_assistant_files(assistant_id: str, organization: str):
    assistant_files = files.find(
        {"assistant_id": assistant_id, "organization": organization})

    items = []
    async for item in assistant_files:
        i = {
            "id": str(item["_id"]),
            "name": item["name"],
            "assistant_id": item["assistant_id"],
            "slug": item.get("slug", ""),
            "file_type": item["file_type"],
            "file": item["file"],
        }
        items.append(i)
    return items


async def get_assistant_file(assistant_id: str, organization: str):
    assistant_file = await files.find_one({"assistant_id": assistant_id, organization: organization})
    if assistant_file:
        return AssistantFile(**assistant_file)
    return None


async def create_assistant_file(assistant_file: AssistantFile):

    existing_assistant_file = await get_assistant_file(assistant_file.assistant_id, assistant_file.organization)
    if existing_assistant_file:
        raise Exception("Assistant file already exists")

    await files.insert_one(assistant_file.dict())

    assistant_file_db = await get_assistant_file(assistant_file.assistant_id, organization=assistant_file.organization)
    return assistant_file_db


async def delete_assistant_file(assistant_id: str, file_type: str):
    try:
        await files.delete_one({"assistant_id": assistant_id, "file_type": file_type})
        return True
    except Exception as e:
        raise e
