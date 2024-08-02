from core.db import apikeys
from core.security import generate_api_key
from src.apikey.models import ApiKey, ApiKeyResponse


async def create_api_key(organization: str):
    api_key = ApiKey(key=generate_api_key(
        {"organization": organization}), organization=organization)
    await apikeys.insert_one(api_key.dict())
    return ApiKeyResponse(apikey=f"ai_{api_key.key}")
