from sqlalchemy import String, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base

class RevokedTokenJTI(Base):
    __tablename__ = "revoked_token_jti"
    __table_args__ = (
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(INTEGER, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    jti: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    exp: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship("User", backref="revoked_jtis")
