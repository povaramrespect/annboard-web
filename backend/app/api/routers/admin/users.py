from fastapi import APIRouter, Depends, Form, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.models import *
from app.crud import *
from app.api.deps import *
from app.core.exceptions import *

admin_router = APIRouter(
    prefix="/admin/users",
    tags=["admin-users"],
    dependencies=[Depends(admin())]
)


@admin_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user_with_role(
    payload: UserCreate, db_session: AsyncSession = Depends(get_db)
):
    crud = UserCRUD(db_session)
    db_user = await crud.create_user(payload)
    return db_user


@admin_router.get("/", response_model=list[User])
async def get_users(
    offset: int = 0,
    limit: int = 100,
    db_session: AsyncSession = Depends(get_db),
):
    crud = UserCRUD(db_session)
    db_users = await crud.get_users(offset, limit)
    return db_users

moder_router = APIRouter(
    prefix="/v1/moderator/users",
    tags=["moderator-users"],
    dependencies=[Depends(admin_moderator())]
)

@moder_router.patch("/{id}", response_model=UserPublic)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    session: AsyncSession = Depends(get_db),
):
    crud = UserCRUD(session)
    db_user = await crud.update_user(user_id, data)
    return db_user


@moder_router.delete("/{id}")
async def delete_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    crud = UserCRUD(session)
    result = await crud.delete_user(user_id)
    return result


