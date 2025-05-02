from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import date, time, datetime, timedelta
from typing import Optional

from src.models.showtime_model import Showtime
from src.models.movie_model import Movie
from src.models.seat_model import Seat
from src.models.user_model import User, RoleEnum
from src.utils.logger import setup_logger
from src.config.config import get_settings
from src.utils.normalize import normalize_empty_to_none
from src.schema.requests.showtime_request import ShowtimeCreateRequest, ShowtimeUpdateRequest
from src.schema.responses.showtime_response import MovieWithShowtimesGroupedResponse, ShowtimeBriefResponse

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

class ShowtimeService:

    @staticmethod
    def verify_admin(user: User):
        if user.user_role != RoleEnum.admin:
            logger.warning(f"🔐 Acceso denegado: usuario no admin: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins are allowed to perform this action."
            )

    @staticmethod
    async def get_all_showtimes(session: AsyncSession):
        logger.info("📺 Recuperando todas las funciones agrupadas por película")
        result = await session.execute(
            select(Movie).options(joinedload(Movie.showtimes))
        )
        movies = result.unique().scalars().all()

        response = []
        for movie in movies:
            normalize_empty_to_none(movie)
            response.append(
                MovieWithShowtimesGroupedResponse(
                    id=movie.id,
                    title=movie.title,
                    description=movie.description,
                    poster_url=movie.poster_url,
                    duration_minutes=movie.duration_minutes,
                    director=movie.director,
                    showtimes=[
                        ShowtimeBriefResponse(id=st.id, show_datetime=st.show_datetime)
                        for st in movie.showtimes
                    ]
                )
            )
        logger.info(f"🎬 Total de películas con funciones: {len(response)}")
        return response

    @staticmethod
    async def get_showtime_by_id(showtime_id: int, session: AsyncSession):
        logger.info(f"🔍 Buscando función por ID: {showtime_id}")
        result = await session.execute(
            select(Showtime).where(Showtime.id == showtime_id).options(
                joinedload(Showtime.movie),
                joinedload(Showtime.seats)
            )
        )
        showtime = result.unique().scalar_one_or_none()
        if not showtime:
            logger.warning(f"⚠️ Función no encontrada: ID {showtime_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Showtime ID {showtime_id} not found."
            )
        normalize_empty_to_none(showtime)
        return showtime

    @staticmethod
    async def create_showtime(data: ShowtimeCreateRequest, session: AsyncSession, user: User):
        ShowtimeService.verify_admin(user)

        now = datetime.now()
        min_datetime = now + timedelta(minutes=30)

        if data.show_datetime < min_datetime:
            logger.warning("❌ Intento de crear una función con muy poca anticipación o en el pasado")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Showtime must be at least 30 minutes in the future."
            )

        movie_result = await session.execute(select(Movie).where(Movie.id == data.movie_id))
        movie = movie_result.scalar_one_or_none()
        if not movie:
            logger.warning(f"❌ Película no encontrada al crear función: ID {data.movie_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Movie with ID {data.movie_id} not found."
            )

        # Validar si ya existe una función exacta para esa película y horario
        conflict_result = await session.execute(
            select(Showtime).where(
                Showtime.movie_id == data.movie_id,
                Showtime.show_datetime == data.show_datetime
            )
        )
        if conflict_result.scalar_one_or_none():
            logger.warning(f"⚠️ Ya existe una función para la película {data.movie_id} a las {data.show_datetime}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A showtime already exists for this movie at the specified datetime."
            )

        showtime = Showtime(
            movie_id=data.movie_id,
            show_datetime=data.show_datetime
        )
        session.add(showtime)
        await session.flush()

        logger.info(f"🎬 Función creada para película ID {data.movie_id}, generando asientos...")
        rows = ['A', 'B', 'C', 'D', 'E']
        for row in rows:
            for num in range(1, 11):
                session.add(Seat(showtime_id=showtime.id, seat_number=f"{row}{num}", is_reserved=False))

        await session.commit()
        await session.refresh(showtime)
        normalize_empty_to_none(showtime)
        logger.info(f"✅ Función creada con ID {showtime.id}")
        return showtime

    @staticmethod
    async def update_showtime(showtime_id: int, data: ShowtimeUpdateRequest, session: AsyncSession, user: User):
        ShowtimeService.verify_admin(user)

        showtime = await ShowtimeService.get_showtime_by_id(showtime_id, session)

        if data.show_datetime:
            min_datetime = datetime.now() + timedelta(minutes=30)
            if data.show_datetime < min_datetime:
                logger.warning("❌ No se puede actualizar la función a una hora muy próxima o pasada")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Showtime must be at least 30 minutes in the future."
                )

            # Validar duplicidad de horario con la misma película
            conflict_result = await session.execute(
                select(Showtime).where(
                    Showtime.movie_id == showtime.movie_id,
                    Showtime.show_datetime == data.show_datetime,
                    Showtime.id != showtime_id  # evitar colisión consigo mismo
                )
            )
            if conflict_result.scalar_one_or_none():
                logger.warning(f"⚠️ Conflicto al actualizar: función duplicada para película ID {showtime.movie_id} en {data.show_datetime}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Another showtime already exists for this movie at the specified datetime."
                )

        for field, value in data.dict(exclude_unset=True).items():
            setattr(showtime, field, value)

        await session.commit()
        await session.refresh(showtime)
        normalize_empty_to_none(showtime)
        logger.info(f"✏️ Función actualizada ID {showtime.id}")
        return showtime

    @staticmethod
    async def delete_showtime(showtime_id: int, session: AsyncSession, user: User):
        ShowtimeService.verify_admin(user)

        showtime = await ShowtimeService.get_showtime_by_id(showtime_id, session)
        await session.delete(showtime)
        await session.commit()
        logger.info(f"🗑️ Función eliminada ID {showtime.id}")

    @staticmethod
    async def search_showtimes_by_datetime(session: AsyncSession, target_date: date, target_time: Optional[time] = None):
        logger.info(f"🔎 Buscando funciones para el {target_date} {f'a las {target_time}' if target_time else ''}")
        
        now = datetime.now()

        stmt = select(Showtime).options(
            joinedload(Showtime.movie)
        ).where(
            Showtime.show_datetime >= max(now, datetime.combine(target_date, time.min)),
            Showtime.show_datetime <= datetime.combine(target_date, time.max)
        )

        if target_time:
            start_dt = datetime.combine(target_date, target_time)
            end_dt = start_dt + timedelta(minutes=59, seconds=59)
            stmt = stmt.where(Showtime.show_datetime.between(start_dt, end_dt))

        result = await session.execute(stmt)
        showtimes = result.unique().scalars().all()

        if not showtimes:
            logger.warning(f"⚠️ No se encontraron funciones para {target_date} {f'{target_time}' if target_time else ''}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No showtimes found for the specified date and time."
            )

        grouped: dict[int, MovieWithShowtimesGroupedResponse] = {}

        for st in showtimes:
            m = st.movie
            if m.id not in grouped:
                grouped[m.id] = MovieWithShowtimesGroupedResponse(
                    id=m.id,
                    title=m.title,
                    description=m.description,
                    poster_url=m.poster_url,
                    duration_minutes=m.duration_minutes,
                    director=m.director,
                    showtimes=[]
                )
            grouped[m.id].showtimes.append(
                ShowtimeBriefResponse(id=st.id, show_datetime=st.show_datetime)
            )

        logger.info(f"🎯 Funciones encontradas: {len(showtimes)} para {len(grouped)} películas")
        return list(grouped.values())
