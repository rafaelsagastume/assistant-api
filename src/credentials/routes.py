from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status

from core.security import verify_token
from src.credentials.models import (Credentials, CredentialsRequest,
                                    CredentialsResponse)
from src.credentials.querys import (create_credential_db, delete_credential_db,
                                    get_credential_by_id,
                                    get_credential_by_type,
                                    get_list_credentials, update_credential_db)

router = APIRouter(prefix="/credentials", tags=["credentials"])


@router.post("/", response_model=CredentialsResponse)
async def create_credential(credential_request: CredentialsRequest, authorization: dict = Depends(verify_token)):
    if credential_request.type == "custom" and not credential_request.custom_headers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="custom_headers must be provided for custom type")
    try:
        credential_data = credential_request.dict()
        credential_data["organization"] = authorization.get("organization")
        credential = Credentials(**credential_data)
        return await create_credential_db(credential)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{id}", response_model=CredentialsResponse)
async def get_credential_by_id_endpoint(id: str, authorization: dict = Depends(verify_token)):
    credential = await get_credential_by_id(id)
    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
    return credential


@router.get("/type/{type_}", response_model=CredentialsResponse)
async def get_credential_by_type_endpoint(type_: str, authorization: dict = Depends(verify_token)):
    credential = await get_credential_by_type(type_)
    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
    return credential


@router.get("/", response_model=List[CredentialsResponse])
async def list_credentials(authorization: dict = Depends(verify_token)):
    return await get_list_credentials()


@router.put("/{id}", response_model=CredentialsResponse)
async def update_credential(id: str, credential_data: dict = Body(), authorization: dict = Depends(verify_token)):
    if credential_data.get("type") == "custom" and not credential_data.get("custom_headers"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="custom_headers must be provided for custom type")
    try:
        credential_data["organization"] = authorization.get("organization")
        updated_credential = await update_credential_db(id, credential_data)
        if not updated_credential:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
        return updated_credential
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id}", response_model=dict)
async def delete_credential(id: str, authorization: dict = Depends(verify_token)):
    try:
        success = await delete_credential_db(id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
        return {"message": "Credential deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
