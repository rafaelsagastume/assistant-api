from pydantic import BaseModel


class Credentials(BaseModel):
    type: str
    secret_key: str
    base_url: str
