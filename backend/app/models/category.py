from .base import *

if TYPE_CHECKING:
    from .advertisement import Advertisement, Value


class CategoryPropertyLink(SQLModel, table=True):
    __tablename__ = "category_property"  # type: ignore

    category_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("categories.id", name="fk_cp_category"),
            primary_key=True
        )
    )

    property_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("properties.id", name="fk_cp_property"),
            primary_key=True
        )
    )

    is_required: bool = Field(default=False)
    order: int = Field(default=0)


class CategoryPropertyCreate(SQLModel):
    category_id: int
    property_id: int
    is_required: bool = False
    order: int = 0


class CategoryPropertyLinkPublic(SQLModel):
    category_id: int
    property_id: int
    is_required: bool
    order: int


class Category(SQLModel, table=True):
    __tablename__ = "categories"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=255, unique=True)

    parent_id: Optional[int] = Field(
        sa_column=Column(
            Integer,
            ForeignKey("categories.id", name="fk_category_category", ondelete="CASCADE"),
            nullable=True
        )
    )

    parents: list["Category"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Category.id"},
    )
    children: Optional[list["Category"]] = Relationship(back_populates="parents")

    properties: list["Property"] = Relationship(
        back_populates="categories",
        link_model=CategoryPropertyLink
    )
    advertisements: list["Advertisement"] = Relationship(back_populates="category")


class Property(SQLModel, table=True):
    __tablename__ = "properties"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True)
    unit: str | None = Field(max_length=50)
    type: PropertyType = Field(default=PropertyType.TEXT)

    categories: list["Category"] = Relationship(
        back_populates="properties",
        link_model=CategoryPropertyLink
    )
    values: list["Value"] = Relationship(back_populates="property")


class PropertyPublic(SQLModel):
    name: str
    unit: str | None = None
    type: PropertyType


class PropertyUpdate(SQLModel):
    name: str | None = None
    unit: str | None = None
    type: PropertyType | None = None


class CategoryCreate(SQLModel):
    name: str
    parent_id: int | None = None


class CategoryPublic(SQLModel):
    name: str
    parents: list["CategoryPublic"] = []


class CategoryUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    parent_id: int | None = None


class PropertyCreate(SQLModel):
    name: str
    unit: str | None = None
    type: PropertyType = PropertyType.TEXT

