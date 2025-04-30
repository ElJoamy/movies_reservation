from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import uuid
from src.config.config import get_settings
from src.utils.logger import setup_logger

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

def _build_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    to_encode.update({
        "exp": expire,
        "iat": now,
        "jti": str(uuid.uuid4())  # Token ID único
    })

    try:
        encoded_jwt = jwt.encode(to_encode, _SETTINGS.jwt_secret, algorithm=_SETTINGS.jwt_algorithm)
        logger.debug("✅ JWT generado correctamente")
        return encoded_jwt
    except Exception as e:
        logger.error(f"❌ Error generando JWT: {e}")
        raise

def create_access_token(data: dict) -> str:
    return _build_token(
        data,
        timedelta(minutes=_SETTINGS.jwt_expiration_minutes)
    )

def create_refresh_token(data: dict) -> str:
    return _build_token(
        data,
        timedelta(minutes=_SETTINGS.jwt_refresh_expiration_minutes)
    )

def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            _SETTINGS.jwt_secret,
            algorithms=[_SETTINGS.jwt_algorithm]
        )
        logger.debug("🔓 JWT decodificado exitosamente")
        return payload
    except JWTError as e:
        logger.warning(f"⚠️ Token inválido o expirado: {e}")
        return None
