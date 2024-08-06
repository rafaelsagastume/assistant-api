
from fastapi import APIRouter, Depends, HTTPException

from core.security import verify_api_key
from src.chat.manager import create_message_process
from src.chat.models import (MessageRequest, MessageResponse, SessionRequest,
                             SessionResponse)
from src.chat.querys import create_session_process

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/session", response_model=SessionResponse)
async def create_session(req: SessionRequest = Depends()):

    authorization = await verify_api_key(apikey=req.apikey)
    if not authorization:
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        organization = "kateai"
        return await create_session_process(req, organization)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message", response_model=MessageResponse)
async def create_message(data: MessageRequest = Depends()):

    authorization = verify_api_key(apikey=data.apikey)
    if not authorization:
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        res = await create_message_process(data.session_id, data.message)
        return MessageResponse(session_id=data.session_id, message=res)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
