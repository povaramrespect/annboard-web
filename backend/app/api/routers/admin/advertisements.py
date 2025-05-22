from fastapi import APIRouter, Depends, Form, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.models import *
from app.crud import *
from app.api.deps import *
from app.core.exceptions import *

router = APIRouter(
    prefix="/v1/admin/advertisements",
    tags=["admin-advertisements"],
    dependencies=[Depends(admin_moderator())]
)

@router.patch("/")
async def update_advertisement(
    ad_id: UUID,
    payload: AdvertisementUpdate,
    session: AsyncSession = Depends(get_db)
):
    crud = AdvertisementCRUD(session)
    db_ad = await crud.update_advertisement(payload, ad_id)
    return db_ad

@router.delete("/")
async def delete_advertisement(
    ad_id: UUID,
    payload: AdvertisementUpdate,
    session: AsyncSession = Depends(get_db)
):
    crud = AdvertisementCRUD(session)
    db_ad = await crud.update_advertisement(payload, ad_id)
    return db_ad

