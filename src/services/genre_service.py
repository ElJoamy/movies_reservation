from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from src.models.genre_model import Genre
from src.models.user_model import User, RoleEnum
from src.schema.requests.genre_request import GenreCreateRequest, GenreUpdateRequest
from src.utils.logger import setup_logger
from src.config.config import get_settings

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)


class GenreService:
    @staticmethod
    def _verify_admin(user: User):
        if user.user_role != RoleEnum.admin:
            logger.warning("❌ Acción denegada: el usuario no es admin")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins are allowed to perform this action."
            )

    async def get_all_genres(self, session: AsyncSession):
        logger.info("📚 Obteniendo todos los géneros")
        result = await session.execute(select(Genre))
        return result.scalars().all()

    async def create_genre(self, data: GenreCreateRequest, session: AsyncSession, user: User):
        self._verify_admin(user)

        existing = await session.execute(select(Genre).where(Genre.name == data.name))
        if existing.scalar_one_or_none():
            logger.warning(f"⚠️ Ya existe el género: {data.name}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Genre '{data.name}' already exists."
            )

        genre = Genre(name=data.name)
        session.add(genre)
        await session.commit()
        await session.refresh(genre)

        logger.info(f"✅ Género creado: {genre.name}")
        return genre

    async def update_genre(self, genre_id: int, data: GenreUpdateRequest, session: AsyncSession, user: User):
        self._verify_admin(user)

        result = await session.execute(select(Genre).where(Genre.id == genre_id))
        genre = result.scalar_one_or_none()
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with ID {genre_id} not found."
            )

        genre.name = data.name
        await session.commit()
        await session.refresh(genre)
        logger.info(f"✏️ Género actualizado: {genre.name}")
        return genre

    async def delete_genre(self, genre_id: int, session: AsyncSession, user: User):
        self._verify_admin(user)

        result = await session.execute(select(Genre).where(Genre.id == genre_id))
        genre = result.scalar_one_or_none()
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with ID {genre_id} not found."
            )

        await session.delete(genre)
        await session.commit()
        logger.warning(f"🗑️ Género eliminado: {genre.name}")
        return {"detail": "Genre deleted successfully"}
