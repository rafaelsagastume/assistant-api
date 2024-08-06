
from fastapi import APIRouter, Depends, HTTPException

from core.security import verify_token
from src.chat.manager import create_message_process
from src.chat.models import MessageResponse, SessionRequest, SessionResponse
from src.chat.querys import create_session_process

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/session", response_model=SessionResponse)
async def create_session(req: SessionRequest = Depends()):
    try:
        organization = "kateai"
        return await create_session_process(req, organization)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message", response_model=MessageResponse)
async def create_message(session_id: str, message: str):
    try:
        res = await create_message_process(session_id, message)
        return MessageResponse(session_id=session_id, message=res)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
