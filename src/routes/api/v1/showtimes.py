from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, time

from src.config.db_config import get_db
from src.config.config import get_settings
from src.utils.logger import setup_logger
from src.models.user_model import User
from src.security.dependencies import get_current_user, get_current_admin_user
from src.services.showtime_service import ShowtimeService
from src.schema.requests.showtime_request import ShowtimeCreateRequest, ShowtimeUpdateRequest
from src.schema.responses.showtime_response import ShowtimeDetailResponse, MovieWithShowtimesGroupedResponse
from src.schema.examples.showtime_example import (
    showtime_create_examples,
    showtime_update_examples,
    showtime_list_examples,
    showtime_detail_examples,
    showtime_delete_examples
)

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)
router = APIRouter(prefix="/showtimes")
showtime_service = ShowtimeService()

# GET /showtimes
@router.get(
    "/",
    response_model=List[MovieWithShowtimesGroupedResponse],
    status_code=200,
    responses=showtime_list_examples,
    tags=["Showtimes"]
)
async def list_showtimes(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    logger.info(f"🎭 Listando todas las funciones disponibles para el usuario {user.email}")
    return await showtime_service.get_all_showtimes(session)

# GET /showtimes/search
@router.get(
    "/search",
    response_model=List[MovieWithShowtimesGroupedResponse],
    status_code=200,
    tags=["Showtimes"]
)
async def search_showtimes(
    date: date = Query(..., description="Fecha en formato YYYY-MM-DD"),
    time: Optional[time] = Query(None, description="Hora en formato HH:MM (24h, opcional)"),
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    logger.info(f"🔎 {user.email} busca funciones para {date} {f'a las {time}' if time else ''}")
    return await showtime_service.search_showtimes_by_datetime(session, date, time)

# GET /showtimes/{id}
@router.get(
    "/{showtime_id}",
    response_model=ShowtimeDetailResponse,
    status_code=200,
    responses=showtime_detail_examples,
    tags=["Showtimes"]
)
async def get_showtime_detail(
    showtime_id: int, 
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    logger.info(f"🔍 Detalle solicitado para la función ID {showtime_id} por {user.email}")
    return await showtime_service.get_showtime_by_id(showtime_id, session)

# POST /showtimes
@router.post(
    "/",
    response_model=ShowtimeDetailResponse,
    status_code=status.HTTP_201_CREATED,
    responses=showtime_create_examples,
    tags=["Admin"]
)
async def create_showtime(
    showtime: ShowtimeCreateRequest,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    admin_user: User = Depends(get_current_admin_user)
):
    logger.info(f"🎬 Creando nueva función para película ID {showtime.movie_id} por admin {admin_user.email}")
    return await showtime_service.create_showtime(showtime, session, admin_user)

# PUT /showtimes/{id}
@router.put(
    "/{showtime_id}",
    response_model=ShowtimeDetailResponse,
    responses=showtime_update_examples,
    tags=["Admin"]
)
async def update_showtime(
    showtime_id: int,
    showtime_data: ShowtimeUpdateRequest,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    admin_user: User = Depends(get_current_admin_user)
):
    logger.info(f"✏️ Actualizando función ID {showtime_id} por admin {admin_user.email}")
    return await showtime_service.update_showtime(showtime_id, showtime_data, session, admin_user)

# DELETE /showtimes/{id}
@router.delete(
    "/{showtime_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=showtime_delete_examples,
    tags=["Admin"]
)
async def delete_showtime(
    showtime_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    admin_user: User = Depends(get_current_admin_user)
):
    logger.warning(f"🗑️ Eliminando función ID {showtime_id} por admin {admin_user.email}")
    await showtime_service.delete_showtime(showtime_id, session, admin_user)
    return
