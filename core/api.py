from openai import AsyncOpenAI

from core.config import OPENAI_API_KEY

client_ai = AsyncOpenAI(api_key=OPENAI_API_KEY)
