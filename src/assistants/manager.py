from core.manager.assistants import create_assistant
from src.assistants.models import Assistant
from src.assistants.querys import create_assistant_db


async def register_assistant(assistant: Assistant, organization: str):
    try:
        assistant_data = await create_assistant(assistant.name, assistant.type, assistant.instructions, organization)

        assistant_class = Assistant(name=assistant.name, type=assistant.type, instructions=assistant.instructions,
                                    organization=organization, assistant_id=assistant_data.id)

        assistant_db = await create_assistant_db(assistant_class)
        return assistant_db
    except Exception as e:
        raise e
