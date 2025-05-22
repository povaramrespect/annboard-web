from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum as PgEnum
from sqlalchemy.dialects.postgresql import UUID as pgUUID
import sqlalchemy as sa
from enum import Enum
from pydantic import EmailStr, SecretStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy.types import TypeDecorator, String


class PropertyType(Enum):
    TEXT = "text"
    NUMBER = "number"
    FLOAT = "float"
    BOOL = "bool"

class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"

class PhoneNumberType(TypeDecorator):
    impl = String

    def process_bind_param(self, value: PhoneNumber | str | None, dialect):
        if value is None:
            return None
        if value.startswith("tel:"):
            value = value[4:]
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if value.startswith("tel:"):
            value = value[4:]
        return PhoneNumber(value)