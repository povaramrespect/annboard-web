from fastapi import APIRouter, Depends, Form, status, Request, UploadFile, File
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.models import *
from app.crud.user_crud import UserCRUD
from app.api.deps import *
from app.core.exceptions import *
from app.core.s3 import s3_client

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/creat22e", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user_with_role(
    payload: UserCreate, db_session: AsyncSession = Depends(get_db)
):
    crud = UserCRUD(db_session)
    db_user = await crud.create_user(payload)
    return db_user

@router.get("/me", response_model=UserMe)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=User) 
async def create_user(
    payload: UserSignup, db_session: AsyncSession = Depends(get_db)
):
    crud = UserCRUD(db_session)
    user = await crud.create_user(payload)
    return user

@router.get("/{id}", response_model=UserPublic)
async def get_user(
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(admin_moderator())
):
    crud = UserCRUD(db_session)
    db_user = await crud.get_user_by_id(id)
    if not db_user:
        raise NotFoundHTTPException(msg="User not found")
    return db_user

@router.get("/", response_model=list[User])
async def get_users(
    offset: int = 0,
    limit: int = 100,
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.moderator, UserRole.admin))
):
    crud = UserCRUD(db_session)
    db_users = await crud.get_users(offset, limit)
    return db_users

@router.patch("/me", response_model=UserPublic)
async def update_myself(
    data: UserUpdate,
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    crud = UserCRUD(db_session)
    user = await crud.update_user(current_user.id, data)
    return user

@router.delete("/{id}")
async def delete_user(
    id: UUID,
    db_session: AsyncSession = Depends(get_db)
):
    crud = UserCRUD(db_session)
    result = await crud.delete_user(id)

    return result

@router.post("/image")
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")

    crud = UserCRUD(session)

    try:
        file_key = f"users/{current_user.id}/{uuid4()}.jpg"
        file_url = await s3_client.upload_file(file, file_key)

        updated_user = await crud.update_image(current_user.id, file_url)
        return {"url": updated_user.avatar_url}

    except Exception as e:
        raise HTTPException(500, f"Upload error: {str(e)}")
