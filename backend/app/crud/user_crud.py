from uuid import UUID
from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import EmailStr
from app.models import User, UserSignup, UserUpdate

from app.core.exceptions import BadRequestHTTPException, NotFoundHTTPException, ForbiddenHTTPException, InternalServerError
from app.core.security import get_password_hash
from app.models import UserCreate


class UserCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    # get by ...

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: EmailStr) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_phone(self, phone: str) -> User | None:
        result = await self.db.execute(select(User).where(User.phone == phone))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    # create, update, delete, get list

    async def create_user(self, user_data: UserSignup | UserCreate) -> User | None:
        if await self.get_user_by_email(user_data.email):
            raise BadRequestHTTPException(msg="Email already in use")

        if await self.get_user_by_username(user_data.username):
            raise BadRequestHTTPException(msg="Username already taken")

        if await self.get_user_by_phone(user_data.phone):
            raise BadRequestHTTPException(msg="Phone already in use")

        hashed_password = get_password_hash(user_data.password.get_secret_value())
        user = User(
            **user_data.model_dump(exclude={"password"}),
            hashed_password=hashed_password,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(
            self,
            user_id: UUID,
            update_data: UserUpdate,
            current_user: Optional[User] = None
    ) -> User | None:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise NotFoundHTTPException(msg="User not found")

        if current_user and current_user.id != user_id:
            raise ForbiddenHTTPException(msg="Cannot update another user")

        update_dict = update_data.model_dump(exclude_unset=True)

        if "email" in update_dict:
            existing = await self.get_user_by_email(update_dict["email"])
            if existing and existing.id != user_id:
                raise BadRequestHTTPException(msg="Email already in use")

        if "username" in update_dict:
            existing = await self.get_user_by_username(update_dict["username"])
            if existing and existing.id != user_id:
                raise BadRequestHTTPException(msg="Username already taken")

        for key, value in update_dict.items():
            setattr(user, key, value)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: UUID) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise NotFoundHTTPException(msg="User not found")
            
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def get_users(
            self,
            offset: int = 0,
            limit: int = 100,
    ): 
        query = select(User).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_image(self, user_id: UUID, file_url: str) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise NotFoundHTTPException(msg="User not found")

        user.avatar_url = file_url

        self.db.add(user)
        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            await self.db.rollback()
            raise InternalServerError(msg="Failed to update user image")