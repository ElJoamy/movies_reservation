from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.config.db_config import get_db
from src.security.dependencies import get_current_user
from src.models.user_model import User
from src.services.profile_service import ProfileService
from src.schema.requests.update_profile_request import UpdateProfileRequest
from src.schema.responses.user_profile_response import UserProfileResponse
from src.dependencies.profile_dependencies import get_update_profile_data
from src.schema.examples.profile_response_example import get_profile_example
from src.schema.examples.update_profile_example import update_profile_example
from src.utils.logger import setup_logger
from src.config.config import get_settings
import imghdr

# Setup
_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

router = APIRouter()
profile_service = ProfileService()


@router.get(
    "/profile",
    response_model=UserProfileResponse,
    responses=get_profile_example,
    description="Returns user profile information",
)
async def get_profile(current_user: User = Depends(get_current_user)):
    logger.info(f"👤 Profile fetch requested by user ID {current_user.id}")
    return await profile_service.get_profile(current_user)


@router.put(
    "/profile",
    response_model=UserProfileResponse,
    responses=update_profile_example,
    description="Updates user profile information",
)
async def update_profile(
    update_data: UpdateProfileRequest = Depends(get_update_profile_data),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"✏️ Update profile requested by user ID {current_user.id}")
    return await profile_service.update_profile(current_user, update_data, db)


@router.get("/profile/photo/{user_id}", description="Returns user profile photo")
async def get_profile_photo(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.debug(f"📸 Photo fetch request by user ID {current_user.id} for user ID {user_id}")

    if user_id != current_user.id:
        logger.warning(f"🚫 Access denied: user {current_user.id} tried to access photo of user {user_id}")
        raise HTTPException(status_code=403, detail="Access denied. You can only view your own profile photo.")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.profile_photo:
        logger.warning(f"📷 Profile photo not found for user ID {user_id}")
        raise HTTPException(status_code=404, detail="Profile photo not found")

    mime_type = imghdr.what(None, h=user.profile_photo)
    if mime_type == "jpeg":
        content_type = "image/jpeg"
    elif mime_type == "png":
        content_type = "image/png"
    elif mime_type in {"heic", "heif"}:
        content_type = "image/heic"
    else:
        content_type = "application/octet-stream"

    logger.info(f"📤 Returning profile photo for user ID {user_id} with MIME type {content_type}")
    return Response(content=user.profile_photo, media_type=content_type)
