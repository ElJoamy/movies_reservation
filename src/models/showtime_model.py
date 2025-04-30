from sqlalchemy import ForeignKey, TIMESTAMP, DATETIME, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base

class Showtime(Base):
    __tablename__ = "showtime"
    __table_args__ = (
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(INTEGER, ForeignKey("movie.id", ondelete="CASCADE"), nullable=False)
    show_datetime: Mapped[str] = mapped_column(DATETIME, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    movie = relationship("Movie", back_populates="showtimes")
    seats = relationship("Seat", back_populates="showtime", cascade="all, delete")
