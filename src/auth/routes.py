from fastapi import APIRouter, Depends, HTTPException

from core.security import (create_access_token, get_password_hash,
                           verify_password, verify_token)
from src.auth.models import Organization, User, UserRegister, UserResponse
from src.auth.querys import create_organization, create_user, get_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(user: UserRegister = Depends()):
    try:
        existing_user = await get_user(user.email)
        if existing_user is not None:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = get_password_hash(user.password)

        organization = Organization(name=user.organization_name, domain=user.organization_domain,
                                    description=user.organization_description)
        await create_organization(organization)

        user = User(username=user.username, password=hashed_password,
                    email=user.email, organization_domain=user.organization_domain)

        await create_user(user)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
