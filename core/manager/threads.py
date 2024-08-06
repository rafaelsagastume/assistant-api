import asyncio

from core.api import client_ai


async def create_thread(assistant_id: str, organization: str):
    thread = await client_ai.beta.threads.create(
        metadata={
            "assistant_id": assistant_id,
            "organization": organization}
    )
    return thread


async def create_thread_message(thread_id: str, message: str):
    thread = await client_ai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )
    return thread


async def run_assistant(assistant_id: str, thread_id: str):
    run = await client_ai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    while run.status == "queued" or run.status == "in_progress":
        run = await client_ai.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread_id)
        await asyncio.sleep(0.4)

    message_response = await client_ai.beta.threads.messages.list(
        thread_id=thread_id,
        order="desc",
        limit=1,
    )

    return message_response.data[0].content[0].text.value
