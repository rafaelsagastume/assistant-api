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
