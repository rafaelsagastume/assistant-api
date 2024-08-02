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
    organization_domain: str


class UserResponse(BaseModel):
    username: str
    email: str
    organization_domain: str


class Organization(BaseModel):
    name: str
    domain: str
    description: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    email: str
    password: str
