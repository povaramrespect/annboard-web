from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import NotFoundHTTPException, InternalServerError
from app.models import *
from .category_crud import CategoryCRUD
from .user_crud import UserCRUD

class AdvertisementCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create_ad(self, payload: AdvertisementCreate, user_id: UUID):
        cat_crud = CategoryCRUD(self.db)
        category = await cat_crud.get_category_by_id(payload.category_id)
        if not category:
            raise NotFoundHTTPException("Category not found")


        ad = Advertisement(**payload.model_dump(exclude={"owner_id"}), owner_id=user_id)


        self.db.add(ad)
        await self.db.commit()
        await self.db.refresh(ad)

        pub_ad = await self.get_advertisement_details(ad.id)

        return pub_ad

    async def get_advertisement_by_id(self, ad_id: UUID) -> Optional[Advertisement]:
        result = await self.db.execute(select(Advertisement).where(Advertisement.id == ad_id))
        return result.scalar_one_or_none()

    async def get_advertisement_details(self, ad_id: UUID):
        query = (
            select(Advertisement)
            .where(Advertisement.id == ad_id)
            .options(
                selectinload(Advertisement.owner),
                selectinload(Advertisement.category),
                selectinload(Advertisement.values).selectinload(Value.property)
            )
        )
        result = await self.db.execute(query)
        ad = result.scalars().first()
        if not ad:
            raise NotFoundHTTPException(msg="Advertisement not found")

        category_crud = CategoryCRUD(self.db)
        parents = await category_crud.get_category_parents(ad.category)

        category_data = ad.category.model_dump()
        category_data["parents"] = [CategoryPublic(**p.model_dump()) for p in parents]

        category_with_parents = CategoryPublic(**category_data)

        ad_public = AdvertisementPublic(
            id=ad.id,
            title=ad.title,
            description=ad.description,
            price=ad.price,
            is_price_negotiable=ad.is_price_negotiable,
            created_at=ad.created_at,
            updated_at=ad.updated_at,
            owner=ad.owner,
            categories=category_with_parents,
            values=ad.values,
        )
        print(category_with_parents)
        return ad_public

    async def get_list_preview(
            self,
            offset: int = 0,
            limit: int = 100,
            search: Optional[str] = None,
    ):
        query = select(Advertisement).offset(offset).limit(limit)
        result = await self.db.execute(query)
        rows = result.scalars().all()

        return rows

    async def create_advertisement_value(
            self,
            payload: ValueCreate
    ):
        category_crud = CategoryCRUD(self.db)
        if not await self.get_advertisement_by_id(payload.advertisement_id):
            raise NotFoundHTTPException(msg="Advertisement not found")

        if not await category_crud.get_property_by_id(payload.property_id):
            raise NotFoundHTTPException(msg="Property not found")

        value = Value(**payload.model_dump())
        self.db.add(value)
        await self.db.commit()
        await self.db.refresh(value)
        return value

    async def delete_advertisement(self, ad_id: UUID):
        ad = await self.get_advertisement_by_id(ad_id)
        if not ad:
            raise NotFoundHTTPException(msg="Advertisement not found")

        await self.db.delete(ad)
        await self.db.commit()
        return True

    async def update_advertisement(self, payload: AdvertisementUpdate, ad_id: UUID):
        ad = await self.get_advertisement_by_id(ad_id)
        if not ad:
            raise NotFoundHTTPException(msg="Advertisement not found")

        update_dict = payload.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(ad, key, value)

        self.db.add(ad)
        await self.db.commit()
        await self.db.refresh(ad)
        return ad

    async def add_image(self, ad_id: UUID, file_url: str) -> Image:
        ad = await self.db.get(Advertisement, ad_id)
        if not ad:
            raise NotFoundHTTPException(msg="Advertisement not found")

        image = Image(url=file_url, advertisement_id=ad_id)

        self.db.add(image)
        try:
            await self.db.commit()
            await self.db.refresh(image)
            return image
        except Exception:
            await self.db.rollback()
            raise InternalServerError(msg="Failed to add image to advertisement")
