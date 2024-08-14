from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status

from core.security import verify_token
from src.functions.models import Function, FunctionRequest, FunctionResponse
from src.functions.querys import (create_function_db, delete_function_db,
                                  get_function_by_id, get_function_by_name,
                                  get_list_functions, update_function_db)

router = APIRouter(prefix="/functions", tags=["functions"])


@router.post("/", response_model=FunctionResponse)
async def create_function(function_request: FunctionRequest, authorization: dict = Depends(verify_token)):
    try:
        function_data = function_request.dict()
        function_data["organization"] = authorization.get("organization")
        function = Function(**function_data)
        return await create_function_db(function)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{id}", response_model=FunctionResponse)
async def get_function_by_id_endpoint(id: str, authorization: dict = Depends(verify_token)):
    function = await get_function_by_id(id)
    if not function:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Function not found")
    return function


@router.get("/name/{name}", response_model=FunctionResponse)
async def get_function_by_name_endpoint(name: str, authorization: dict = Depends(verify_token)):
    function = await get_function_by_name(name)
    if not function:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Function not found")
    return function


@router.get("/", response_model=List[FunctionResponse])
async def list_functions(authorization: dict = Depends(verify_token)):
    return await get_list_functions()


@router.put("/{id}", response_model=FunctionResponse)
async def update_function(id: str, function_data: dict = Body(), authorization: dict = Depends(verify_token)):
    try:
        function_data["organization"] = authorization.get("organization")
        updated_function = await update_function_db(id, function_data)
        if not updated_function:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Function not found")
        return updated_function
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id}", response_model=dict)
async def delete_function(id: str, authorization: dict = Depends(verify_token)):
    try:
        success = await delete_function_db(id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Function not found")
        return {"message": "Function deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
