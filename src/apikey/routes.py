from typing import List

from fastapi import APIRouter, Depends, HTTPException

from core.security import verify_token
from src.apikey.models import ApiKeyResponse
from src.apikey.querys import create_api_key, delete_api_key, list_api_keys

router = APIRouter(prefix="/apikey", tags=["apikey"])


@router.post("/generate", response_model=ApiKeyResponse)
async def create(authorization: dict = Depends(verify_token)):

    print(authorization)

    try:
        organization = authorization.organization
        return await create_api_key(organization)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=List[ApiKeyResponse])
async def list(authorization: dict = Depends(verify_token)):

    try:
        organization = authorization.organization
        return await list_api_keys(organization)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{apikey}", response_model=ApiKeyResponse)
async def delete(apikey: str, authorization: dict = Depends(verify_token)):

    try:
        organization = authorization.organization
        await delete_api_key(organization, apikey)
        return ApiKeyResponse(apikey=f"ai_{apikey}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
