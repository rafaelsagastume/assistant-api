from pydantic import BaseModel


class Assistant(BaseModel):
    name: str
    type: str
    instructions: str
    organization: str
    assistant_id: str


class AssistantRequest(BaseModel):
    id: str = None
    name: str
    type: str
    instructions: str
