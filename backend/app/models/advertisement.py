from .base import *

from .user import User, UserPublic, UserPreview
from .category import Category, Property, CategoryPublic, PropertyPublic
from .image import Image

class AdvertisementBase(SQLModel):
    title: str = Field(max_length=255)
    description: str = Field(max_length=1000)
    price: Decimal | None = Field(
        ge=1,
        default=None,
        max_digits=12,
        decimal_places=2,
        nullable=True
    )
    is_price_negotiable: bool = Field(default=False)


class Advertisement(AdvertisementBase, table=True):
    __tablename__ = "advertisements"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    owner_id: UUID | None = Field(
        sa_column=Column(
            pgUUID(as_uuid=True),
            ForeignKey("users.id", name="fk_advertisements_owner_id", ondelete="CASCADE"),
            nullable=True
        )
    )

    category_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("categories.id", name="fk_advertisements_category_id", ondelete="SET NULL"),
            nullable=False
        )
    )

    images: list["Image"] = Relationship(back_populates="advertisement", sa_relationship_kwargs={"lazy": "selectin"})
    owner: "User" = Relationship(back_populates="advertisements", sa_relationship_kwargs={"lazy": "selectin"})
    category: "Category" = Relationship(back_populates="advertisements", sa_relationship_kwargs={"lazy": "selectin"})
    values: List["Value"] = Relationship(back_populates="advertisement", sa_relationship_kwargs={"lazy": "selectin"})


class Value(SQLModel, table=True):
    __tablename__ = "values"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    advertisement_id: UUID = Field(
        sa_column=Column(
            pgUUID(as_uuid=True),
            ForeignKey("advertisements.id", name="fk_values_advertisement", ondelete="CASCADE"),
            nullable=False
        )
    )

    property_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("properties.id", name="fk_values_properties", ondelete="CASCADE"),
            nullable=False
        )
    )

    value: str

    advertisement: "Advertisement" = Relationship(back_populates="values", sa_relationship_kwargs={"lazy": "selectin"})
    property: "Property" = Relationship(back_populates="values", sa_relationship_kwargs={"lazy": "selectin"})


class ValueCreate(SQLModel):
    advertisement_id: UUID
    property_id: int
    value: str


class ValuePublic(SQLModel):
    value: str
    property: "PropertyPublic"


class AdvertisementUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    price: Decimal | None = Field(
        default=None,
        max_digits=12,
        decimal_places=2,
        nullable=True
    )
    is_price_negotiable: bool | None = Field(default=None)


class AdvertisementPublic(AdvertisementBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None
    owner: "UserPublic"
    is_price_negotiable: bool
    categories: "CategoryPublic"
    values: list["ValuePublic"] | None = None

class AdvertisementCreate(AdvertisementBase):
    # owner_id: UUID
    category_id: int


class AdvertisementPreview(SQLModel):
    id: UUID
    title: str
    price: Decimal | None
    owner: "UserPreview"
    created_at: datetime


class ListAdvertisementsPreview(SQLModel):
    advertisements: list[AdvertisementPreview]
