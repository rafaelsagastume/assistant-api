from core.db import threads
from core.manager.threads import create_thread
from src.assistants.querys import get_assistant_by_id
from src.chat.models import Session, SessionRequest, SessionResponse


async def create_session_process(req: SessionRequest, organization: str) -> SessionResponse:
    thread = await create_thread(req.assistant_db_id, organization)
    assistant = await get_assistant_by_id(req.assistant_db_id)

    if not assistant:
        raise Exception("Assistant not found")

    new_session = Session(
        assistant_id=assistant.assistant_id,
        thread_id=thread.id,
        organization=organization
    )
    session_result = await threads.insert_one(new_session.dict())

    return SessionResponse(session_id=str(session_result.inserted_id))
