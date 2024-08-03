from pydantic import BaseModel


class Assistant(BaseModel):
    name: str
    instructions: str
    organization: str
    assistant_id: str


class AssistantRequest(BaseModel):
    name: str
    instructions: str


class AssistantResponse(BaseModel):
    id: str
    name: str
    instructions: str
    organization: str
