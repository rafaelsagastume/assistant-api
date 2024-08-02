from core.db import apikeys
from core.security import generate_api_key
from src.apikey.models import ApiKey, ApiKeyResponse


async def create_api_key(organization: str):
    api_key = ApiKey(key=generate_api_key(
        {"organization": organization}), organization=organization)
    await apikeys.insert_one(api_key.dict())
    return ApiKeyResponse(apikey=f"ai_{api_key.key}")


async def list_api_keys(organization: str):
    api_keys = apikeys.find({"organization": organization})

    items = []
    async for item in api_keys:
        items.append(ApiKeyResponse(apikey=f"ai_{item['key']}"))
    return items


async def delete_api_key(organization: str, apikey: str):
    await apikeys.delete_one({"organization": organization, "key": apikey})
