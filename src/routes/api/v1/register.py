from fastapi import APIRouter, Depends, status
from src.config.db_config import get_db
from src.services.register_service import RegisterService
from src.schema.requests.register_request import RegisterRequest
from src.schema.responses.user_register_response import UserRegisterResponse
from src.schema.examples.register_example import register_examples
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.logger import setup_logger
from src.config.config import get_settings

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

router = APIRouter()
register_service = RegisterService()

@router.post(
    "/register",
    response_model=UserRegisterResponse,
    responses=register_examples,
    status_code=status.HTTP_201_CREATED,
    description="Register a new user"
)
async def register_user(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    logger.debug("🛎️ Received request at /register")
    return await register_service.register_user(db, request)
