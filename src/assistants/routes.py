from typing import List

from fastapi import APIRouter, Depends, HTTPException

from core.security import verify_token
from src.assistants.manager import delete_assistant_by_id, register_assistant
from src.assistants.models import AssistantRequest, AssistantResponse
from src.assistants.querys import get_list_assistants

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


@router.get("/list", response_model=List[AssistantResponse])
async def list(authorization: dict = Depends(verify_token)):
    try:
        organization = authorization.organization
        return await get_list_assistants(organization)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{id}", response_model=bool)
async def delete(id: str, authorization: dict = Depends(verify_token)):
    try:
        organization = authorization.organization
        return await delete_assistant_by_id(id, organization)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
