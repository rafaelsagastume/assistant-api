import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

token_auth_scheme = APIKeyHeader(name="Authorization", auto_error=False)
api_key_auth_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


class TokenData(BaseModel):
    username: Optional[str] = None
    organization: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_api_key(data: dict):
    unique_suffix = str(uuid.uuid4())
    to_encode = data.copy()
    to_encode.update(
        {"unique_id": unique_suffix})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(token_auth_scheme)):

    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        organization = payload.get("organization")
        if username is None or organization is None:
            raise credentials_exception
        token_data = TokenData(username=username, organization=organization)
    except JWTError:
        raise credentials_exception
    return token_data


def verify_api_key(apikey: str = Depends(api_key_auth_scheme)):

    if apikey.startswith("ai_"):
        apikey = apikey.split("ai_")[1]
    else:
        raise HTTPException(status_code=401, detail="Invalid API key format")

    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate API key"
    )

    if not apikey:
        raise credentials_exception

    try:
        payload = jwt.decode(apikey, SECRET_KEY, algorithms=[ALGORITHM])
        organization = payload.get("organization")
        if organization is None:
            raise credentials_exception
        token_data = TokenData(organization=organization)
    except JWTError as e:
        print(e)
        raise credentials_exception
    return token_data
