from fastapi import APIRouter, Depends, status, Response, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.db_config import get_db
from src.services.login_service import LoginService
from src.schema.requests.login_request import LoginRequest
from src.schema.responses.token_response import TokenResponse
from src.security.jwt_handler import decode_token
from src.utils.logger import setup_logger
from src.config.config import get_settings

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

router = APIRouter()
login_service = LoginService()

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    description="Authenticate user and set tokens in secure HttpOnly cookies"
)
async def login_user(
    request: Request,
    body: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    # 🔒 Verificar si ya está logueado por cookie
    existing_token = request.cookies.get(_SETTINGS.jwt_cookie_name)
    if existing_token:
        decoded = decode_token(existing_token)
        if decoded:
            logger.info(f"🔁 Login rejected — already authenticated (user_id={decoded.get('sub')})")
            raise HTTPException(status_code=400, detail="You are already logged in.")

    logger.debug(f"🛎️ Received login request for {body.email}")
    return await login_service.login_user(db, body, response)
