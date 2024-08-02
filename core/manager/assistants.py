from core.api import client_ai


async def create_assistant(name: str, type: str, instructions: str, organization: str):
    assistant = await client_ai.beta.assistants.create(
        model="gpt-4o-mini",
        name=name,
        instructions=instructions,
        metadata={"organization": organization},
    )
    return assistant
