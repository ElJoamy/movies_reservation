from typing import Optional

from sqlalchemy import Index, String, TIMESTAMP, text, Column, Enum
from sqlalchemy.dialects.mysql import INTEGER, LONGBLOB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.models.base_model import Base
import datetime
import enum

class RoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        Index('country_code', 'country_code', 'phone_number', unique=True),
        Index('email', 'email', unique=True),
        {
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_unicode_ci"
        }
    )

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    lastname: Mapped[str] = mapped_column(String(100))
    nickname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    country_code: Mapped[str] = mapped_column(String(6))
    phone_number: Mapped[str] = mapped_column(String(20))
    country: Mapped[str] = mapped_column(String(100))
    profile_photo: Mapped[Optional[bytes]] = mapped_column(LONGBLOB)
    user_role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.user, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
