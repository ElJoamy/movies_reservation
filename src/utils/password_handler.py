from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from src.utils.logger import setup_logger
from src.config.config import get_settings

# Obtener configuración y configurar logger
_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

# Instancia de hasher
ph = PasswordHasher()

def hash_password(password: str) -> str:
    """Hash a plain password using Argon2"""
    hashed = ph.hash(password)
    logger.debug("Password hashed successfully.")
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed version"""
    try:
        result = ph.verify(hashed_password, plain_password)
        logger.debug("Password verified correctly.")
        return result
    except VerifyMismatchError:
        logger.warning("Password verification failed: mismatch.")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during password verification: {e}")
        return False
