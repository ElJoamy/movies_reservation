from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import INTEGER
from src.models.base_model import Base

class MovieGenre(Base):
    __tablename__ = "movie_genre"
    __table_args__ = (
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    movie_id: Mapped[int] = mapped_column(INTEGER, ForeignKey("movie.id", ondelete="CASCADE"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(INTEGER, ForeignKey("genre.id", ondelete="CASCADE"), primary_key=True)
