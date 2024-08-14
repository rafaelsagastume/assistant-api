from typing import List

from bson import ObjectId

from core.db import credentials
from src.credentials.models import Credentials, CredentialsResponse


async def get_credential_by_id(id: str) -> CredentialsResponse:
    credential = await credentials.find_one({"_id": ObjectId(id)})
    if credential:
        return CredentialsResponse(
            id=str(credential["_id"]),
            type=credential["type"],
            base_url=credential["base_url"],
            organization=credential["organization"],
        )
    return None


async def get_credential_by_type(type_: str) -> CredentialsResponse:
    credential = await credentials.find_one({"type": type_})
    if credential:
        return CredentialsResponse(
            id=str(credential["_id"]),
            type=credential["type"],
            base_url=credential["base_url"],
            organization=credential["organization"],
        )
    return None


async def create_credential_db(credential: Credentials) -> CredentialsResponse:
    if credential.type == "custom" and not credential.custom_headers:
        raise ValueError("custom_headers must be provided for custom type")

    existing_credential = await get_credential_by_type(credential.type)
    if existing_credential:
        raise Exception("Credential already exists")

    result = await credentials.insert_one(credential.dict())
    created_credential = await get_credential_by_id(str(result.inserted_id))
    return created_credential


async def get_list_credentials() -> List[CredentialsResponse]:
    credentials_cursor = credentials.find()
    items = []
    async for item in credentials_cursor:
        items.append(CredentialsResponse(
            id=str(item["_id"]),
            type=item["type"],
            base_url=item["base_url"],
            organization=item["organization"]
        ))
    return items


async def update_credential_db(id: str, credential_data: dict) -> CredentialsResponse:
    if credential_data.get("type") == "custom" and not credential_data.get("custom_headers"):
        raise ValueError("custom_headers must be provided for custom type")

    try:
        await credentials.update_one({"_id": ObjectId(id)}, {"$set": credential_data})
        updated_credential = await get_credential_by_id(id)
        return updated_credential
    except Exception as e:
        raise e


async def delete_credential_db(id: str) -> bool:
    try:
        result = await credentials.delete_one({"_id": ObjectId(id)})
        return result.deleted_count == 1
    except Exception as e:
        raise e
