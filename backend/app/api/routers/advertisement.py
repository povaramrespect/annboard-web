from fastapi import APIRouter, Depends, Form, status, Request, UploadFile, File
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.models import *
from app.crud.advertisement_crud import AdvertisementCRUD
from app.core.s3 import s3_client
from app.core.exceptions import *
from app.api.deps import *

router = APIRouter(tags=["advertisements"])

@router.post("/advertisement", status_code=status.HTTP_201_CREATED, response_model=AdvertisementPublic)
async def create_advertisement(
    payload: AdvertisementCreate,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    # payload.owner_id = current_user.id
    crud = AdvertisementCRUD(db_session)
    db_ad = await crud.create_ad(payload, current_user.id)
    return db_ad

@router.get("/advertisement/{id}", response_model=AdvertisementPublic)
async def get_advertisement(
    id: UUID,
    db_session: AsyncSession = Depends(get_db)
):
    crud = AdvertisementCRUD(db_session)
    db_ad = await crud.get_advertisement_details(id)
    return db_ad

@router.get("/advertisements", response_model=list[AdvertisementPreview])
async def get_ads_preview(
    search: str | None = None,
    offset: int = 0,
    limit: int = 100,
    db_session: AsyncSession = Depends(get_db)
):
    crud = AdvertisementCRUD(db_session)
    ads = await crud.get_list_preview(
        search=search,
        offset=offset,
        limit=limit,
    )
    return ads

@router.delete("/{id}")
async def delete_ad(
    ad_id: UUID,
    db_session: AsyncSession = Depends(get_db)
):
    crud = AdvertisementCRUD(db_session)
    await crud.delete_advertisement(ad_id)

    return True

@router.post("/advertisement/{id}/add_value", response_model=ValuePublic)
async def add_value(
    payload: ValueCreate,
    session: AsyncSession = Depends(get_db)
):
    crud = AdvertisementCRUD(session)
    value = await crud.create_advertisement_value(payload)
    return value

@router.post("/advertisement/{id}/upload-image")
async def upload_ad_image(
    ad_id: UUID,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")

    crud = AdvertisementCRUD(session)
    try:
        file_key = f"advertisements/{ad_id}/{uuid4()}.jpg"
        file_url = await s3_client.upload_file(file, file_key)

        image = await crud.add_image(ad_id=ad_id, file_url=file_url)
        return {"id": image.id, "url": image.url}

    except Exception as e:
        raise HTTPException(500, f"Upload error: {str(e)}")



@router.patch("/advertisement/{id}", response_model=AdvertisementPublic)
async def update_ad(

):
    # id: UUID,
    # data: Advertisement,
    # db_session: AsyncSession = Depends(get_db)

    return True


# @router.get("/{id}") #, response_model=AdvertisementPublic
# async def get_my_advertisements():

#     return True