from fastapi import APIRouter, Depends, HTTPException

from core.security import verify_token
from src.apikey.models import ApiKeyResponse
from src.apikey.querys import create_api_key

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
