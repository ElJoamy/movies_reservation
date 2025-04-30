from sqlalchemy import ForeignKey, String, Text, TIMESTAMP, SMALLINT, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base
from src.models.genre_model import Genre
from src.models.movie_genre_model import MovieGenre

class Movie(Base):
    __tablename__ = "movie"
    __table_args__ = (
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    year: Mapped[int] = mapped_column(SMALLINT, nullable=True) 
    duration_minutes: Mapped[int] = mapped_column(SMALLINT, nullable=True) 
    director: Mapped[str] = mapped_column(String(255), nullable=True)
    poster_url: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    genres = relationship("Genre", secondary="movie_genre", back_populates="movies") 
    showtimes = relationship("Showtime", back_populates="movie", cascade="all, delete")
