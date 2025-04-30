from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.config.db_config import get_db
from src.config.config import get_settings
from src.utils.logger import setup_logger
from src.models.user_model import User
from src.security.dependencies import get_current_user, get_current_admin_user
from src.services.movie_service import MovieService
from src.schema.requests.movie_request import MovieCreateRequest, MovieUpdateRequest
from src.schema.responses.movie_response import MovieResponse, MovieWithShowtimesResponse
from src.schema.examples.movie_example import (
    movie_create_examples,
    movie_update_examples,
    movie_list_examples,
    movie_detail_examples,
    movie_delete_examples
)

# Configuración y logger
_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

router = APIRouter(prefix="/movies")
movie_service = MovieService()

# GET /movies
@router.get(
    "/",
    response_model=List[MovieResponse],
    status_code=200,
    responses=movie_list_examples,
    tags=["Movies"]
)
async def list_movies(session: AsyncSession = Depends(get_db)):
    logger.info("🎬 Listando todas las películas")
    return await movie_service.get_all_movies(session)

# GET /movies/{id}
@router.get(
    "/{movie_id}",
    response_model=MovieWithShowtimesResponse,
    status_code=200,
    responses=movie_detail_examples,
    tags=["Movies"]
)
async def get_movie_detail(movie_id: int, session: AsyncSession = Depends(get_db)):
    logger.info(f"🎞️ Obteniendo detalle de película {movie_id}")
    return await movie_service.get_movie_by_id(movie_id, session)

# POST /movies
@router.post(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
    responses=movie_create_examples,
    tags=["Admin"]
)
async def create_new_movie(
    movie: MovieCreateRequest,
    session: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    logger.info(f"➕ Creando película: {movie.title}")
    return await movie_service.create_movie(movie, session, admin_user)

# PUT /movies/{id}
@router.put(
    "/{movie_id}",
    response_model=MovieResponse,
    responses=movie_update_examples,
    tags=["Admin"]
)
async def update_movie_detail(
    movie_id: int,
    movie_data: MovieUpdateRequest,
    session: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    logger.info(f"✏️ Actualizando película ID {movie_id}")
    return await movie_service.update_movie(movie_id, movie_data, session, admin_user)

# DELETE /movies/{id}
@router.delete(
    "/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=movie_delete_examples,
    tags=["Admin"]
)
async def delete_movie_by_id(
    movie_id: int,
    session: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    logger.warning(f"❌ Eliminando película ID {movie_id}")
    await movie_service.delete_movie(movie_id, session, admin_user)
    return

# GET /movies/by-genre/{genre_id}
@router.get(
    "/by-genre/{genre_id}",
    response_model=List[MovieResponse],
    status_code=200,
    tags=["Movies"]
)
async def list_movies_by_genre(
    genre_id: int,
    session: AsyncSession = Depends(get_db)
):
    logger.info(f"🎯 Buscando películas por género ID {genre_id}")
    return await movie_service.get_movies_by_genre(genre_id, session)
