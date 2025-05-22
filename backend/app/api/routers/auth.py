from fastapi import APIRouter, Depends, Form, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.models.user import UserPublic, UserSignup, User, UserUpdate, UserLogin
from app.crud.user_crud import UserCRUD

from app.api.deps import authenticate_user
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(get_db)
):
    token = await authenticate_user(username, password, session)
    return {"access_token": token, "token_type": "bearer"}



