from fastapi import HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from datetime import datetime, timezone
from src.models.user_model import User
from src.models.revoked_token_jti_model import RevokedTokenJTI
from src.security.jwt_handler import decode_token, create_access_token, create_refresh_token
from src.config.config import get_settings
from src.utils.logger import setup_logger

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

class RefreshTokenService:
    async def rotate_tokens(self, request: Request, response: Response, db: AsyncSession) -> dict:
        refresh_token = request.cookies.get(_SETTINGS.jwt_refresh_cookie_name)

        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token missing")

        payload = decode_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        user_id = payload.get("sub")
        jti = payload.get("jti")
        exp = payload.get("exp")

        if not user_id or not jti or not exp:
            raise HTTPException(status_code=401, detail="Invalid refresh token payload")

        # Verificar si ya fue revocado
        result = await db.execute(select(RevokedTokenJTI).where(RevokedTokenJTI.jti == jti))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=401, detail="Refresh token already used")

        # Verificar existencia de usuario
        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Revocar token usado
        await db.execute(insert(RevokedTokenJTI).values(
            user_id=user.id,
            jti=jti,
            exp=datetime.fromtimestamp(exp, tz=timezone.utc)
        ))

        # Crear tokens nuevos
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        new_payload = decode_token(refresh_token)

        # Setear cookies nuevas
        response.set_cookie(_SETTINGS.jwt_cookie_name, access_token, httponly=True, secure=_SETTINGS.jwt_cookie_secure, samesite=_SETTINGS.jwt_cookie_samesite, max_age=_SETTINGS.jwt_expiration_minutes * 60)
        response.set_cookie(_SETTINGS.jwt_refresh_cookie_name, refresh_token, httponly=True, secure=_SETTINGS.jwt_cookie_secure, samesite=_SETTINGS.jwt_cookie_samesite, max_age=_SETTINGS.jwt_refresh_expiration_minutes * 60)

        logger.info(f"♻️ Token rotated for user {user.email}")
        return {
            "message": "Tokens refreshed successfully.",
            "jti": new_payload.get("jti")
        }

    def issue_tokens(self, user_id: int, response: Response) -> tuple[str, str]:
        access_token = create_access_token({"sub": str(user_id)})
        refresh_token = create_refresh_token({"sub": str(user_id)})

        response.set_cookie(
            key=_SETTINGS.jwt_cookie_name,
            value=access_token,
            httponly=True,
            samesite=_SETTINGS.jwt_cookie_samesite,
            secure=_SETTINGS.jwt_cookie_secure,
            max_age=_SETTINGS.jwt_expiration_minutes * 60
        )

        response.set_cookie(
            key=_SETTINGS.jwt_refresh_cookie_name,
            value=refresh_token,
            httponly=True,
            samesite=_SETTINGS.jwt_cookie_samesite,
            secure=_SETTINGS.jwt_cookie_secure,
            max_age=_SETTINGS.jwt_refresh_expiration_minutes * 60
        )

        return access_token, refresh_token

    async def revoke_current_refresh_token(self, request: Request, db: AsyncSession, user_id: int):
        token = request.cookies.get(_SETTINGS.jwt_refresh_cookie_name)
        if not token:
            return

        payload = decode_token(token)
        jti = payload.get("jti")
        exp = payload.get("exp")

        if jti and exp:
            await db.execute(insert(RevokedTokenJTI).values(
                user_id=user_id,
                jti=jti,
                exp=datetime.fromtimestamp(exp, tz=timezone.utc)
            ))
            await db.commit()