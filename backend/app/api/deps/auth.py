from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.crud.user_crud import UserCRUD
from app.core.db import get_db
from app.core.exceptions import AuthFailedHTTPException
from app.core.security import verify_password, create_access_token

import logging

logger = logging.getLogger("uvicorn")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db)
) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise AuthFailedHTTPException(msg="Invalid authentication credentials")
    user_id = payload.get("sub")
    if user_id is None:
        raise AuthFailedHTTPException(msg="Invalid authentication credentials")

    user_crud = UserCRUD(session)
    user = await user_crud.get_user_by_id(user_id)
    if not user:
        raise AuthFailedHTTPException(msg="User not found")
    return user

async def authenticate_user(
    username: str,
    password: str,
    session: AsyncSession,
) -> str:
    user_crud = UserCRUD(session)
    user = await user_crud.get_user_by_username(username)  # метод для поиска юзера по логину/емейлу
    if not user:
        raise AuthFailedHTTPException(msg="Invalid credentials")
    if not verify_password(password, user.hashed_password):
        raise AuthFailedHTTPException(msg="Invalid credentials")
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    return access_token