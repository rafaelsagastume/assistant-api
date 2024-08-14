from fastapi import APIRouter, Depends, HTTPException, status, Body
from src.credentials.querys import (
    get_credential_by_id,
    get_credential_by_type,
    create_credential_db,
    get_list_credentials,
    update_credential_db,
    delete_credential_db,
)
from src.credentials.models import Credentials
from core.security import verify_token
from typing import List


router = APIRouter(prefix="/credentials", tags=["credentials"])


@router.post("/", response_model=Credentials)
async def create_credential(credential: Credentials, authorization: dict = Depends(verify_token)):
    if credential.type == "custom" and not credential.custom_headers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="custom_headers must be provided for custom type")
    try:
        return await create_credential_db(credential)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{id}", response_model=Credentials)
async def get_credential_by_id_endpoint(id: str, authorization: dict = Depends(verify_token)):
    credential = await get_credential_by_id(id)
    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
    return credential


@router.get("/type/{type_}", response_model=Credentials)
async def get_credential_by_type_endpoint(type_: str, authorization: dict = Depends(verify_token)):
    credential = await get_credential_by_type(type_)
    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
    return credential


@router.get("/", response_model=List[Credentials])
async def list_credentials(authorization: dict = Depends(verify_token)):
    return await get_list_credentials()


@router.put("/{id}", response_model=Credentials)
async def update_credential(id: str, credential_data: dict = Body(), authorization: dict = Depends(verify_token)):
    if credential_data.get("type") == "custom" and not credential_data.get("custom_headers"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="custom_headers must be provided for custom type")
    try:
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
