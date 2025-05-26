from .base import *

if TYPE_CHECKING:
    from advertisement import Advertisement, AdvertisementPreview
    from image import Image

class UserBase(SQLModel):
    username: str = Field(unique=True, max_length=50, index=True)


class UserSignup(UserBase):
    email: EmailStr
    phone: PhoneNumber
    password: SecretStr


class UserCreate(UserBase):
    email: EmailStr
    phone: PhoneNumber
    password: SecretStr
    role: UserRole


class UserUpdate(SQLModel):  # Me
    username: str | None = Field(None, max_length=50)
    phone: PhoneNumber | None = Field(None)
    email: EmailStr | None = Field(None, max_length=255)


class UserUpdatePassword(SQLModel):
    password: SecretStr | None = Field(None, max_length=20)


class User(UserBase, table=True):
    __tablename__ = "users"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    phone: PhoneNumber = Field(
        sa_column=Column(
            PhoneNumberType(),
            nullable=True,
        )
    )
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    email: EmailStr = Field(max_length=255, index=True)
    hashed_password: str
    email_verified: bool = Field(default=False)
    role: UserRole = Field(
        sa_column=Column(
            PgEnum(UserRole, name="userrole"),
            nullable=False,
            default=UserRole.user
        )
    )
    avatar_url: str = Field(nullable=True)
    advertisements: list["Advertisement"] = Relationship(back_populates="owner")

    profile_img: "Image" = Relationship(back_populates="user") #, sa_relationship_kwargs={"lazy": "selectin"}

class UserPublic(UserBase):
    id: UUID
    phone: PhoneNumber
    # advertisements: list["AdvertisementPreview"]


class UserLogin(UserBase):
    password: SecretStr


class UserPreview(UserBase):
    profile_img: "Image" | None


class UserMe(UserPublic):
    email: EmailStr
    phone: PhoneNumber
    email_verified: bool = Field(default=False)


class Users(SQLModel):
    data: list[User]
    count: int

class UserUpdatePhoto(SQLModel):
    avatar_url: str