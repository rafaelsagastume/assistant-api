from core.db import organizations, users
from src.auth.models import Organization, User


async def get_user(email: str):
    user = await users.find_one({"email": email})
    if user:
        return User(**user)
    return None


async def get_organization(domain: str):
    organization = await organizations.find_one({"domain": domain})
    if organization:
        return Organization(**organization)
    return None


async def create_user(user: User):

    existing_user = await get_user(user.email)
    if existing_user:
        raise Exception("User already exists")

    existing_organization = await get_organization(user.organization_domain)
    if not existing_organization:
        raise Exception("Organization does not exist")

    await users.insert_one(user.dict())


async def create_organization(organization: Organization):

    existing_organization = await get_organization(organization.domain)
    if existing_organization:
        raise Exception("Organization already exists")

    await organizations.insert_one(organization.dict())
