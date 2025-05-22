from fastapi import APIRouter, Depends, Form, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.models import *
from app.crud import CategoryCRUD

router = APIRouter(tags=["category"])

@router.post("/category", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(
    payload: CategoryCreate,
    session: AsyncSession = Depends(get_db),
    ):
    crud = CategoryCRUD(session)
    category = await crud.create_category(payload)

    return category

@router.get("/category", response_model=list[Category])
async def get_categories(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db)
):
    crud = CategoryCRUD(session)
    categories = await crud.get_categories(
        offset=offset,
        limit=limit,
    )
    return categories

@router.delete("/category/{id}", status_code=status.HTTP_200_OK)
async def delete_category(id: int, session: AsyncSession = Depends(get_db)):
    crud = CategoryCRUD(session)
    result = await crud.delete_category(id)
    return result

@router.patch("/category/{id}", status_code=status.HTTP_200_OK)
async def update_category(
    id: int, 
    payload: CategoryUpdate,
    session: AsyncSession = Depends(get_db)
):
    crud = CategoryCRUD(session)
    category = await crud.update_category(payload, id)
    return category

@router.post("/property", response_model=Property, status_code=status.HTTP_201_CREATED)
async def create_property(
    payload: PropertyCreate,
    session: AsyncSession = Depends(get_db)
) -> Property:
    crud = CategoryCRUD(session)
    prop = await crud.create_property(payload)
    return prop

@router.get("/properties", response_model=list[Property])
async def get_properties(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db)
):
    crud = CategoryCRUD(session)
    properties = await crud.get_properties(offset, limit)
    return properties

@router.post("/add_property", response_model=CategoryPropertyLinkPublic, status_code=status.HTTP_201_CREATED)
async def attach_property_to_category(
    payload: CategoryPropertyCreate, 
    session: AsyncSession = Depends(get_db)
):
    crud = CategoryCRUD(session)
    link = await crud.attach_property_to_category(payload)
    return link

@router.get("/category_property", response_model=list[CategoryPropertyLink])
async def get_links(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db)
):
    crud = CategoryCRUD(session)
    links = await crud.get_category_property_links(offset, limit)
    return links
