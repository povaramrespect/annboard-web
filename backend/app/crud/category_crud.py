from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import *

from app.core.exceptions import BadRequestHTTPException, NotFoundHTTPException


class CategoryCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_category_by_name(self, name: str):
        result = await self.db.execute(select(Category).where(Category.name == name))
        return result.scalar_one_or_none()

    async def get_category_by_id(self, id: int):
        result = await self.db.execute(select(Category).where(Category.id == id))
        return result.scalar_one_or_none()

    async def get_category_parents(self, category: Category):
        categories = []
        current = category
        while current.parent_id:
            query = select(Category).where(Category.id == current.parent_id)
            result = await self.db.execute(query)
            current = result.scalar_one_or_none()
            if current:
                categories.append(CategoryPublic.from_orm(current))
            else:
                break
        return categories[::-1] 


    async def create_category(self, payload: CategoryCreate) -> Category:
        if await self.get_category_by_name(payload.name):
            raise BadRequestHTTPException(msg="Category with this name already exists")

        if payload.parent_id:

            parent = await self.get_category_by_id(payload.parent_id)
            if not parent:
                raise BadRequestHTTPException(msg="Parent category with this id does not exist")

        category = Category(**payload.model_dump())
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category
    
    async def delete_category(self, id: int) -> bool:
        category = await self.get_category_by_id(id)
        if not category:
            raise NotFoundHTTPException(msg="Category with this id does not exists")
        
        await self.db.delete(category)
        await self.db.commit()
        return True

    async def get_categories(
        self,   
        offset: int,
        limit: int,
    ):
        query = select(Category).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_category(
        self,
        id: int,
        payload: CategoryUpdate,
    ) -> Category:
        category = await self.get_category_by_id(id)
        if not category:
            raise NotFoundHTTPException(msg="Category not found")
        
        update_dict = payload.model_dump(exclude_unset=True)
        if "name" in update_dict:
            if await self.get_category_by_name(update_dict["name"]):
                raise BadRequestHTTPException(msg="Category with this name already exists")
        
        if "parent_id" in update_dict:
            parent = await self.get_category_by_id(update_dict["parent_id"])
            if not parent:
                raise BadRequestHTTPException(msg="Parent category with this id does not exist")

        for key, value in update_dict.items():
            setattr(category, key, value)

        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def get_property_by_name(self, name: str):
        result = await self.db.execute(select(Property).where(Property.name == name))
        return result.scalar_one_or_none()

    async def get_property_by_id(self, id: int):
        result = await self.db.execute(select(Property).where(Property.id == id))
        return result.scalar_one_or_none()

    async def create_property(self, payload: PropertyCreate):
        if await self.get_property_by_name(payload.name):
            raise BadRequestHTTPException(msg="Property with this name exists")
        
        prop = Property(**payload.model_dump())
        self.db.add(prop)
        await self.db.commit()
        await self.db.refresh(prop)
        return prop

    async def update_property(
        self,
        update_data: PropertyUpdate,
        property_id: int,
    ) -> User | None:
        prop = await self.get_property_by_id(property_id)
        if not prop:
            raise NotFoundHTTPException(msg="Property not found")

        update_dict = update_data.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(prop, key, value)

        self.db.add(prop)
        await self.db.commit()
        await self.db.refresh(prop)
        return prop

    async def delete_property(self, property_id: int) -> bool:
        prop = await self.get_property_by_id(property_id)
        if not prop:
            raise NotFoundHTTPException(msg="Category with this id does not exists")

        await self.db.delete(prop)
        await self.db.commit()
        return True

    async def get_properties(
        self,
        offset: int,
        limit: int,
    ): 
        query = select(Property).offset(offset).limit(limit)
        properties = await self.db.execute(query)
        return properties.scalars().all()

    async def attach_property_to_category(
        self,
        payload: CategoryPropertyCreate,
    ):
        if not await self.get_category_by_id(payload.category_id):
            raise NotFoundHTTPException(msg="Category not found")
        
        if not await self.get_property_by_id(payload.property_id):
            raise NotFoundHTTPException(msg="Property not found")
        
        link = CategoryPropertyLink(**payload.model_dump())
        self.db.add(link)
        await self.db.commit()
        await self.db.refresh(link)
        return link       
    
    async def get_category_property_links(
        self,
        offset: int,
        limit: int
    ):
        query = select(CategoryPropertyLink).offset(offset).limit(limit)
        links = await self.db.execute(query)
        return links.scalars().all()