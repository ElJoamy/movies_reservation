from sqlalchemy import ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base

class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    failed_attempts: Mapped[int] = mapped_column(INTEGER, default=0)
    last_failed_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)

    user = relationship("User", backref="login_attempt")
