from fastapi import HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user_model import User
from src.schema.requests.login_request import LoginRequest
from src.schema.responses.token_response import TokenResponse
from src.utils.password_handler import verify_password
from src.utils.login_attempt_handler import (
    check_login_attempts,
    increment_login_attempts,
    reset_login_attempts
)
from src.services.refresh_token_service import RefreshTokenService
from src.security.jwt_handler import decode_token
from src.utils.logger import setup_logger
from src.config.config import get_settings

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

class LoginService:
    async def login_user(self, db: AsyncSession, credentials: LoginRequest, response: Response) -> TokenResponse:
        logger.info(f"🔐 Login attempt for email: {credentials.email}")

        # Buscar usuario
        result = await db.execute(select(User).where(User.email == credentials.email))
        user = result.scalar_one_or_none()

        if not user:
            logger.warning(f"❌ Login failed - user not found: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Verificar intentos fallidos
        await check_login_attempts(db, user.id)

        # Verificar contraseña
        if not verify_password(credentials.password, user.password):
            logger.warning(f"❌ Login failed - incorrect password for: {credentials.email}")
            await increment_login_attempts(db, user.id)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Resetear contador de intentos
        await reset_login_attempts(db, user.id)

        # Generar tokens + setear cookies usando el servicio dedicado
        refresh_service = RefreshTokenService()
        access_token, refresh_token = refresh_service.issue_tokens(user.id, response)

        # Extraer jti para respuesta
        decoded = decode_token(access_token)
        jti = decoded.get("jti", "unknown")

        logger.info(f"✅ Login successful for user ID {user.id} ({user.email}) — JTI: {jti}")
        return TokenResponse(message="Login successful.", jti=jti)
