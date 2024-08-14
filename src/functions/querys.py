from typing import List

from bson import ObjectId

from core.db import functions
from src.functions.models import Function, FunctionResponse


async def get_function_by_id(id: str) -> FunctionResponse:
    function = await functions.find_one({"_id": ObjectId(id)})
    if function:
        return FunctionResponse(**function, id=str(function["_id"]))
    return None


async def get_function_by_name(name: str) -> FunctionResponse:
    function = await functions.find_one({"name": name})
    if function:
        return FunctionResponse(**function, id=str(function["_id"]))
    return None


async def create_function_db(function: Function) -> FunctionResponse:
    existing_function = await get_function_by_name(function.name)
    if existing_function:
        raise Exception("Function already exists")

    result = await functions.insert_one(function.dict())
    created_function = await get_function_by_id(str(result.inserted_id))
    return created_function


async def get_list_functions() -> List[FunctionResponse]:
    functions_cursor = functions.find()
    items = []
    async for item in functions_cursor:
        items.append(FunctionResponse(**item, id=str(item["_id"])))
    return items


async def update_function_db(id: str, function_data: dict) -> FunctionResponse:
    try:
        await functions.update_one({"_id": ObjectId(id)}, {"$set": function_data})
        updated_function = await get_function_by_id(id)
        return updated_function
    except Exception as e:
        raise e


async def delete_function_db(id: str) -> bool:
    try:
        result = await functions.delete_one({"_id": ObjectId(id)})
        return result.deleted_count == 1
    except Exception as e:
        raise e
