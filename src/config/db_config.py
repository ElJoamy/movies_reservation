import logging
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from src.config.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__, level=logging.DEBUG)

# Solo evalúa settings en ejecución real
try:
    _SETTINGS = get_settings()
except Exception:
    _SETTINGS = None
    logger.warning("⚠️ No se pudieron cargar las variables de entorno (get_settings())")

# Construir URL solo si settings existen
if _SETTINGS:
    SQLALCHEMY_DATABASE_URL = (
        f"mysql+aiomysql://{_SETTINGS.db_user}:{_SETTINGS.db_password}"
        f"@{_SETTINGS.db_host}:{_SETTINGS.db_port}/{_SETTINGS.db_name}"
        f"?charset=utf8mb4"
    )

    # Validación de variables
    if not all([_SETTINGS.db_user, _SETTINGS.db_password, _SETTINGS.db_host, _SETTINGS.db_port, _SETTINGS.db_name]):
        logger.error("❌ No se han definido las variables de entorno de la base de datos")
    else:
        logger.info("Variables de entorno de la base de datos configuradas")
    
    # Crear motor y sesión solo si hay configuración válida
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=50,
        max_overflow=50,
        pool_timeout=60,
        pool_recycle=3600,
        echo=False,
    )

    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
else:
    # Dummy fallback para que pdoc no crashee
    engine = None
    async_session = None

Base = declarative_base()

# Dependency para FastAPI
async def get_db():
    if not async_session:
        raise RuntimeError("La sesión async no está configurada.")
    async with async_session() as session:
        yield session

# Script de prueba opcional
if __name__ == "__main__" and engine:
    async def test_connection():
        try:
            logger.info("🔄 Iniciando conexión a la base de datos...")
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
                logger.info("✅ Conexión a la base de datos establecida correctamente.")
        except Exception as e:
            logger.error(f"❌ Error al conectar con la base de datos: {e}")

    asyncio.run(test_connection())
