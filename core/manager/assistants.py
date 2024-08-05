from core.api import client_ai


async def create_assistant(name: str, instructions: str, organization: str):
    assistant = await client_ai.beta.assistants.create(
        model="gpt-4o-mini",
        name=name,
        instructions=instructions,
        metadata={"organization": organization},
        tools=[
            {"type": "code_interpreter"},
            {"type": "file_search"},
        ],
    )
    return assistant


async def delete_assistant(assistant_id: str):
    try:
        await client_ai.beta.assistants.delete(assistant_id)
        return True
    except Exception as e:
        raise e


async def update_assistant_assignment_vector_store(assistant_id: str, vector_store_id: str):
    try:
        await client_ai.beta.assistants.update(
            assistant_id=assistant_id,
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store_id]
                }
            }
        )
        return True
    except Exception as e:
        raise e
