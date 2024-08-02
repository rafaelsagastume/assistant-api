from pydantic import BaseModel


class ApiKey(BaseModel):
    key: str
    organization: str


class ApiKeyResponse(BaseModel):
    apikey: str
