from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.config.db_config import get_db
from src.models.user_model import User
from src.models.revoked_token_jti_model import RevokedTokenJTI
from src.security.jwt_handler import decode_token
from src.utils.logger import setup_logger
from src.config.config import get_settings
from src.models.user_model import RoleEnum

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    token = request.cookies.get(_SETTINGS.jwt_cookie_name)

    if not token:
        logger.warning("❌ No access token found in cookies")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    payload = decode_token(token)
    if not payload:
        logger.warning("❌ Invalid or expired token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = payload.get("sub")
    jti = payload.get("jti")

    if not user_id or not str(user_id).isdigit() or not jti:
        logger.error("❌ Invalid token payload structure")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    # 🔒 Revisar si el jti ha sido revocado
    result = await db.execute(select(RevokedTokenJTI).where(RevokedTokenJTI.jti == jti))
    if result.scalar_one_or_none():
        logger.warning(f"🚫 Token with jti {jti} has been revoked")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        logger.warning(f"❌ User with ID {user_id} not found")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

async def get_current_admin_user(
    user: User = Depends(get_current_user)
) -> User:
    if user.user_role != RoleEnum.admin:
        logger.warning(f"🔒 Access denied for user {user.id} — not admin")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return user