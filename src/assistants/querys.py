from core.db import assitants
from src.assistants.models import Assistant


async def get_assistant_db(assistant_id: str):
    assistant = await assitants.find_one({"assistant_id": assistant_id})
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
