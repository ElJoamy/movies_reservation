from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import status
import secrets
from src.config.config import get_settings
from src.utils.logger import setup_logger

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

EXCLUDED_PATHS = {"/api/v1/login", "/api/v1/register", "/api/v1/token/refresh", "/docs", "/openapi.json", "/api/v1/logout", "/favicon.ico"}  # agrega aquí los que quieras excluir

class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Excluir rutas seguras (login, register, etc.)
        if (
            request.method not in _SETTINGS.csrf_safe_methods and
            request.url.path not in EXCLUDED_PATHS
        ):
            csrf_cookie = request.cookies.get(_SETTINGS.csrf_cookie_name)
            csrf_header = request.headers.get(_SETTINGS.csrf_header_name)

            if not csrf_cookie or not csrf_header or csrf_cookie != csrf_header:
                logger.warning(f"🚫 CSRF validation failed — Cookie: {csrf_cookie}, Header: {csrf_header}")
                return Response(
                    content="CSRF validation failed",
                    status_code=status.HTTP_403_FORBIDDEN
                )

        response: Response = await call_next(request)

        # Setear CSRF token si no existe aún
        if _SETTINGS.csrf_cookie_name not in request.cookies:
            token = secrets.token_urlsafe(32)
            logger.debug("🔐 Setting new CSRF token cookie")
            response.set_cookie(
                key=_SETTINGS.csrf_cookie_name,
                value=token,
                httponly=False,
                samesite="strict",
                max_age=_SETTINGS.csrf_cookie_expire_minutes * 60
            )

        return response
