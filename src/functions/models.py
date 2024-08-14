from pydantic import BaseModel


class Function(BaseModel):
    assistant_id: str
    name: str
    description: str
    type_request: str
    json_schema: dict
    organization: str


class FunctionRequest(BaseModel):
    assistant_id: str
    name: str
    description: str
    type_request: str
    json_schema: dict


class FunctionResponse(BaseModel):
    id: str
    name: str
    description: str
    type_request: str
    json_schema: dict
    organization: str
