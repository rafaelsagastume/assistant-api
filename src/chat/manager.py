
from core.manager.threads import create_thread_message, run_assistant
from src.chat.querys import get_session_by_id


async def create_message_process(session_id: str, message: str):
    session = await get_session_by_id(session_id)
    if not session:
        raise Exception("Session not found")

    thread = await create_thread_message(session.thread_id, message, session.assistant_id)
    response = await run_assistant(session.assistant_id, session.thread_id)
    return response
