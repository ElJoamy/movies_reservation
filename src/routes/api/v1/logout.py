from fastapi import APIRouter, Response, status, Request, Depends
from src.services.refresh_token_service import RefreshTokenService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from src.utils.logger import setup_logger
from src.config.config import get_settings
from src.security.dependencies import get_current_user
from src.security.jwt_handler import decode_token
from src.models.user_model import User
from src.models.revoked_token_jti_model import RevokedTokenJTI
from src.config.db_config import get_db
from datetime import datetime

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

router = APIRouter()

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Revokes tokens by jti and clears cookies."
)
async def logout_user(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    token = request.cookies.get(_SETTINGS.jwt_cookie_name)
    refresh_service = RefreshTokenService()

    if not token:
        logger.warning("❌ No token in cookie during logout")
        response.delete_cookie(_SETTINGS.jwt_cookie_name)
        response.delete_cookie(_SETTINGS.jwt_refresh_cookie_name)
        return {"message": "No session to log out from."}

    # 🔒 Revocar access_token
    decoded = decode_token(token)
    jti = decoded.get("jti")
    exp_ts = decoded.get("exp")

    if jti and exp_ts:
        exp = datetime.fromtimestamp(exp_ts)
        await db.execute(
            insert(RevokedTokenJTI).values(
                user_id=current_user.id,
                jti=jti,
                exp=exp
            )
        )
        await db.commit()
        logger.info(f"🔒 Access token revoked — JTI: {jti}")

    # 🔒 Revocar refresh_token también
    await refresh_service.revoke_current_refresh_token(request, db, current_user.id)

    # 🧼 Limpiar cookies
    response.delete_cookie(_SETTINGS.jwt_cookie_name)
    response.delete_cookie(_SETTINGS.jwt_refresh_cookie_name)

    logger.info(f"👋 Logout complete for user ID {current_user.id}")
    return {"message": "Logged out successfully."}