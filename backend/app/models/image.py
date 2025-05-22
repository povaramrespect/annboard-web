from .base import *

if TYPE_CHECKING:
    from .advertisement import Advertisement
    from .user import User


class Image(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    url: str
    user_id: UUID | None = Field(default=None, foreign_key="users.id", ondelete="CASCADE")
    advertisement_id: UUID | None = Field(default=None, foreign_key="advertisements.id", ondelete="CASCADE")

    user: Optional["User"] = Relationship(back_populates="profile_img")
    advertisement: Optional["Advertisement"] = Relationship(back_populates="images")
