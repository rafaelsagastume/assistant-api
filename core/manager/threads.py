from core.api import client_ai


async def create_thread(assistant_id: str, organization: str):
    thread = await client_ai.beta.threads.create(
        metadata={
            "assistant_id": assistant_id,
            "organization": organization}
    )
    return thread
