import re

from fastapi import UploadFile
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


class AssistantFile(BaseModel):
    name: str
    assistant_id: str
    slug: str = None
    file_id: str
    organization: str
    vector_id: str

    def __init__(self, **data):
        super().__init__(**data)
        if not self.slug:
            self.slug = self.generate_slug(self.name)

    @staticmethod
    def generate_slug(name: str) -> str:
        slug = re.sub(r'\s+', '-', name.lower()).strip('-')
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        return slug


class AssistantFileRequest(BaseModel):
    name: str
    assistant_id: str
    file: UploadFile


class AssistantVectorStore(BaseModel):
    vector_store_id: str
    assistant_id: str
