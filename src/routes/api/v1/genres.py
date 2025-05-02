from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.config.db_config import get_db
from src.config.config import get_settings
from src.utils.logger import setup_logger
from src.models.user_model import User
from src.security.dependencies import get_current_user
from src.security.dependencies import get_current_admin_user
from src.services.genre_service import GenreService
from src.schema.requests.genre_request import GenreCreateRequest, GenreUpdateRequest
from src.schema.responses.genre_response import GenreResponse
from src.schema.examples.genre_example import (
    genre_create_examples,
    genre_update_examples,
    genre_list_examples,
    genre_detail_examples,
    genre_delete_examples
)

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

router = APIRouter(prefix="/genres")
genre_service = GenreService()

# GET /genres
@router.get(
    "/",
    response_model=List[GenreResponse],
    status_code=200,
    responses=genre_list_examples,
    tags=["Genres"]
)
async def list_genres(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    logger.info("📚 Listando todos los géneros")
    return await genre_service.get_all_genres(session)

# GET /genres/{id}
@router.get(
    "/{genre_id}",
    response_model=GenreResponse,
    status_code=200,
    responses=genre_detail_examples,
    tags=["Genres"]
)
async def get_genre_detail(
    genre_id: int, 
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    logger.info(f"🔎 Obteniendo género ID {genre_id}")
    return await genre_service.get_genre_by_id(genre_id, session)

# POST /genres
@router.post(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED,
    responses=genre_create_examples,
    tags=["Admin"]
)
async def create_genre(
    genre: GenreCreateRequest,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    admin_user: User = Depends(get_current_admin_user)
):
    logger.info(f"🆕 Creando nuevo género: {genre.name}")
    return await genre_service.create_genre(genre, session, admin_user)

# PUT /genres/{genre_id}
@router.put(
    "/{genre_id}",
    response_model=GenreResponse,
    responses=genre_update_examples,
    tags=["Admin"]
)
async def update_genre(
    genre_id: int,
    genre_data: GenreUpdateRequest,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    admin_user: User = Depends(get_current_admin_user)
):
    logger.info(f"✏️ Actualizando género ID {genre_id}")
    return await genre_service.update_genre(genre_id, genre_data, session, admin_user)

# DELETE /genres/{genre_id}
@router.delete(
    "/{genre_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=genre_delete_examples,
    tags=["Admin"]
)
async def delete_genre(
    genre_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    admin_user: User = Depends(get_current_admin_user)
):
    logger.warning(f"🗑️ Eliminando género ID {genre_id}")
    await genre_service.delete_genre(genre_id, session, admin_user)
    return
