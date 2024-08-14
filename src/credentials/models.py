from pydantic import BaseModel


class Credentials(BaseModel):
    type: str
    secret_key: str
    custom_headers: str
    base_url: str
