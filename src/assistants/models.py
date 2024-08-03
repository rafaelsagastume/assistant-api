import re

from pydantic import BaseModel


class Assistant(BaseModel):
    name: str
    instructions: str
    organization: str
    assistant_id: str
    slug: str = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.slug:
            self.slug = self.generate_slug(self.name)

    @staticmethod
    def generate_slug(name: str) -> str:
        slug = re.sub(r'\s+', '-', name.lower()).strip('-')
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        return slug


class AssistantRequest(BaseModel):
    name: str
    instructions: str


class AssistantResponse(BaseModel):
    id: str
    name: str
    instructions: str
    organization: str
    slug: str
