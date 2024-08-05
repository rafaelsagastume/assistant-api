from pydantic import BaseModel


class Session(BaseModel):
    assistant_id: str
    thread_id: str
    organization: str


class SessionRequest(BaseModel):
    assistant_db_id: str


class SessionResponse(BaseModel):
    session_id: str
