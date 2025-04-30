from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from src.security.jwt_handler import decode_token
from src.config.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user_model import User
from src.utils.logger import setup_logger
from src.config.config import get_settings

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("access_token")
        request.state.user = None

        if token:
            payload = decode_token(token)
            if payload:
                user_id = payload.get("sub")
                try:
                    async for db in get_db():
                        result = await db.execute(select(User).where(User.id == int(user_id)))
                        user = result.scalar_one_or_none()
                        if user:
                            request.state.user = user
                            logger.debug(f"✅ User {user.email} injected from session")
                        break
                except Exception as e:
                    logger.error(f"❌ SessionMiddleware error: {e}")

        response: Response = await call_next(request)
        return response
