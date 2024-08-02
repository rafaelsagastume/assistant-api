from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import (create_access_token, get_password_hash,
                           verify_password)
from src.auth.models import (Organization, Token, User, UserLogin,
                             UserRegister, UserResponse)
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


@router.post("/login", response_model=Token)
async def login(user: UserLogin = Depends()):
    try:
        existing_user = await get_user(user.email)
        if existing_user is None:
            raise HTTPException(status_code=400, detail="User not found")

        if not verify_password(user.password, existing_user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": existing_user.email}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
