from sqlalchemy import String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base
from src.models.movie_genre_model import MovieGenre

class Genre(Base):
    __tablename__ = "genre"
    __table_args__ = (
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    movies = relationship("Movie", secondary="movie_genre", back_populates="genres")