from fastapi import APIRouter, Depends, Form, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.models import *
from app.crud import *
from app.api.deps import *
from app.core.exceptions import *

router = APIRouter(
    prefix="/v1/admin/categories",
    tags=["admin-categories"],
    dependencies=[Depends(admin_moderator())]
)

@router.post("/")
async def create_category(
    payload: CategoryCreate,
    session: AsyncSession = Depends(get_db)
):
    crud = CategoryCRUD(session)
    db_category = await crud.create_category(payload)
    return db_category

@router.patch("/{id}")
async def update_category(
    category_id: int,
    payload: CategoryUpdate,
    session: AsyncSession = Depends(get_db)
):
    crud = CategoryCRUD(session)
    db_category = await crud.update_category(payload, category_id)
    return db_category

@router.delete("/{id}")
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_db)
):
    crud = CategoryCRUD(session)
    await crud.delete_category(category_id)
    return True

@router.post("/properties/")
async def create_property(
    payload: PropertyCreate,
    session: AsyncSession = Depends(get_db)
):
    crud = CategoryCRUD(session)
    db_property = await crud.create_property(payload)
    return db_property

@router.patch("/properties/{id}")
async def update_property(
    property_id: int,
    payload: PropertyUpdate,
    session: AsyncSession = Depends(get_db)
):
    crud = CategoryCRUD(session)
    db_property = await crud.update_property(payload, property_id)
    return db_property

@router.delete("/properties/{id}")
async def delete_property(
    property_id: int,
    session: AsyncSession = Depends(get_db)
):
    crud = CategoryCRUD(session)
    await crud.delete_property(property_id)
    return True