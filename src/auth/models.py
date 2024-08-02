import re

from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str
    email: str
    organization_name: str
    organization_domain: str  # example = @damian.com
    organization_description: str


class User(BaseModel):
    username: str
    password: str
    email: str
    organization: str


class UserResponse(BaseModel):
    username: str
    email: str
    organization: str


class Organization(BaseModel):
    name: str
    domain: str
    description: str
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


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    email: str
    password: str
