from fastapi import APIRouter, Depends, HTTPException

from core.security import verify_token
from src.assistants.manager import register_assistant
from src.assistants.models import AssistantRequest

router = APIRouter(prefix="/assistants", tags=["assistants"])


@router.post("/register", response_model=AssistantRequest)
async def register(assistant: AssistantRequest = Depends(), authorization: dict = Depends(verify_token)):
    try:
        organization = authorization.organization
        return await register_assistant(assistant, organization)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
