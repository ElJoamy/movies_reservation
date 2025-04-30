from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status

from src.models.movie_model import Movie
from src.models.genre_model import Genre
from src.models.movie_genre_model import MovieGenre
from src.models.showtime_model import Showtime
from src.schema.requests.movie_request import MovieCreateRequest, MovieUpdateRequest
from src.models.user_model import User, RoleEnum
from src.utils.normalize import normalize_empty_to_none
from src.utils.logger import setup_logger
from src.config.config import get_settings

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

class MovieService:

    @staticmethod
    def verify_admin(user: User):
        if user.user_role != RoleEnum.admin:
            logger.warning(f"🔐 Acceso denegado para usuario {user.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins are allowed to perform this action."
            )

    async def get_all_movies(self, session: AsyncSession):
        logger.debug("📥 Buscando todas las películas con géneros y funciones...")
        result = await session.execute(
            select(Movie).options(
                joinedload(Movie.genres),
                joinedload(Movie.showtimes)
            )
        )
        movies = result.unique().scalars().all()
        for movie in movies:
            normalize_empty_to_none(movie)
        logger.info(f"🎬 {len(movies)} películas encontradas")
        return movies

    async def get_movie_by_id(self, movie_id: int, session: AsyncSession):
        logger.debug(f"🔍 Buscando detalle de película ID {movie_id}")
        result = await session.execute(
            select(Movie).where(Movie.id == movie_id).options(
                joinedload(Movie.genres),
                joinedload(Movie.showtimes)
            )
        )
        movie = result.unique().scalar_one_or_none()
        if not movie:
            logger.warning(f"❌ Película con ID {movie_id} no encontrada")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with ID {movie_id} not found."
            )
        normalize_empty_to_none(movie)
        return movie

    async def create_movie(self, data: MovieCreateRequest, session: AsyncSession, user: User):
        self.verify_admin(user)
        logger.info(f"➕ Creando película: {data.title}")

        movie = Movie(
            title=data.title,
            description=data.description,
            poster_url=data.poster_url,
            year=data.year,
            duration_minutes=data.duration_minutes,
            director=data.director
        )

        session.add(movie)
        await session.flush()

        for genre_id in data.genre_ids:
            genre_result = await session.execute(select(Genre).where(Genre.id == genre_id))
            genre = genre_result.scalar_one_or_none()
            if not genre:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Genre with ID {genre_id} not found."
                )
            session.add(MovieGenre(movie_id=movie.id, genre_id=genre_id))

        await session.commit()
        await session.refresh(movie)
        normalize_empty_to_none(movie)
        return movie

    async def update_movie(self, movie_id: int, data: MovieUpdateRequest, session: AsyncSession, user: User):
        self.verify_admin(user)
        logger.info(f"✏️ Actualizando película ID {movie_id}")

        movie = await self.get_movie_by_id(movie_id, session)

        for field, value in data.dict(exclude_unset=True).items():
            if field != "genre_ids":
                setattr(movie, field, value)

        if data.genre_ids is not None:
            await session.execute(delete(MovieGenre).where(MovieGenre.movie_id == movie.id))

            for genre_id in data.genre_ids:
                genre_result = await session.execute(select(Genre).where(Genre.id == genre_id))
                genre = genre_result.scalar_one_or_none()
                if not genre:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Genre with ID {genre_id} not found."
                    )
                session.add(MovieGenre(movie_id=movie.id, genre_id=genre_id))

        await session.commit()
        await session.refresh(movie)
        normalize_empty_to_none(movie)
        return movie

    async def delete_movie(self, movie_id: int, session: AsyncSession, user: User):
        self.verify_admin(user)
        logger.warning(f"🗑️ Eliminando película ID {movie_id}")
        movie = await self.get_movie_by_id(movie_id, session)
        await session.delete(movie)
        await session.commit()

    async def get_movies_by_genre(self, genre_id: int, session: AsyncSession):
        stmt = (
            select(Movie)
            .join(Movie.genres)
            .where(Genre.id == genre_id)
            .options(
                joinedload(Movie.genres),
                joinedload(Movie.showtimes)
            )
        )
        result = await session.execute(stmt)
        movies = result.unique().scalars().all()

        for movie in movies:
            normalize_empty_to_none(movie)

        return movies
