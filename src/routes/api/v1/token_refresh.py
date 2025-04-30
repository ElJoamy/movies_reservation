from src.services.refresh_token_service import RefreshTokenService
from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.db_config import get_db
from src.config.config import get_settings
from src.utils.logger import setup_logger

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

router = APIRouter()
refresh_service = RefreshTokenService()

@router.post("/token/refresh")
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    return await refresh_service.rotate_tokens(request, response, db)