import logging
from functools import cache
from pydantic_settings import BaseSettings
from src.utils.logger import setup_logger

logger = setup_logger(__name__, level=logging.DEBUG)

class Settings(BaseSettings):
    service_name: str = "Movies Reservation"
    k_revision: str = "local"
    log_level: str = "DEBUG"
    api_url: str = "http://localhost:8000/"

    db_host: str = "localhost"
    db_user: str = "root"
    db_password: str = "root"
    db_port: int = 3306
    db_name: str = "db_name"

    # JWT config
    jwt_secret: str = "your-super-secret-key-that-nobody-knows"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 15            # Access token lifespan
    jwt_refresh_expiration_minutes: int = 43200 # Refresh token lifespan (30 días)

    # Cookie config
    jwt_cookie_name: str = "access_token"
    jwt_refresh_cookie_name: str = "refresh_token"
    jwt_cookie_secure: bool = False             # True si usas HTTPS
    jwt_cookie_samesite: str = "strict"         # strict | lax | none

    # CSRF config
    csrf_cookie_name: str = "csrf_token"
    csrf_header_name: str = "X-CSRF-Token"
    csrf_safe_methods: set[str] = {"HEAD", "OPTIONS"}
    csrf_cookie_expire_minutes: int = 15

    @property
    def debug(self) -> bool:
        return self.log_level.upper() == "DEBUG"

    class Config:
        env_file = ".env"

@cache
def get_settings():
    return Settings()
