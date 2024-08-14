from bson import ObjectId

from core.db import credentials
from src.credentials.models import Credentials


async def get_credential_by_id(id: str):
    credential = await credentials.find_one({"_id": ObjectId(id)})
    if credential:
        return Credentials(**credential)
    return None


async def get_credential_by_type(type_: str):
    credential = await credentials.find_one({"type": type_})
    if credential:
        return Credentials(**credential)
    return None


async def create_credential_db(credential: Credentials):
    if credential.type == "custom" and not credential.custom_headers:
        raise ValueError("custom_headers must be provided for custom type")

    existing_credential = await get_credential_by_type(credential.type)
    if existing_credential:
        raise Exception("Credential already exists")

    await credentials.insert_one(credential.dict())
    created_credential = await get_credential_by_type(credential.type)
    return created_credential


async def get_list_credentials():
    credentials_cursor = credentials.find()

    items = []
    async for item in credentials_cursor:
        i = {
            "id": str(item["_id"]),
            "type": item["type"],
            "secret_key": item["secret_key"],
            "base_url": item["base_url"],
            "custom_headers": item.get("custom_headers"),
        }
        items.append(i)
    return items


async def update_credential_db(id: str, credential_data: dict):
    if credential_data.get("type") == "custom" and not credential_data.get("custom_headers"):
        raise ValueError("custom_headers must be provided for custom type")

    try:
        await credentials.update_one({"_id": ObjectId(id)}, {"$set": credential_data})
        updated_credential = await get_credential_by_id(id)
        return updated_credential
    except Exception as e:
        raise e


async def delete_credential_db(id: str):
    try:
        await credentials.delete_one({"_id": ObjectId(id)})
        return True
    except Exception as e:
        raise e
