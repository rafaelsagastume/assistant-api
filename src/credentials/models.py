from pydantic import BaseModel


class Credentials(BaseModel):
    type: str
    secret_key: str
    custom_headers: str
    base_url: str
    organization: str = None


class CredentialsResponse(BaseModel):
    id: str
    type: str
    base_url: str
    organization: str


class CredentialsRequest(BaseModel):
    type: str
    secret_key: str
    custom_headers: str
    base_url: str
