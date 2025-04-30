from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user_model import User
from src.utils.password_handler import hash_password
from src.schema.requests.update_profile_request import UpdateProfileRequest
from src.utils.logger import setup_logger
from src.config.config import get_settings
from src.utils.validators import (
    validate_country_code,
    validate_phone_number,
    validate_password_strength,
    validate_profile_photo
)

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

class ProfileService:
    async def get_profile(self, user: User):
        return {
            "id": user.id,
            "name": user.name,
            "lastname": user.lastname,
            "nickname": user.nickname,
            "email": user.email,
            "country": user.country,
            "country_code": user.country_code,
            "phone_number": user.phone_number,
            "profile_photo_url": f"/profile/photo/{user.id}" if user.profile_photo else None
        }

    async def update_profile(self, user: User, data: UpdateProfileRequest, db: AsyncSession):
        if data.name:
            user.name = data.name

        if data.lastname:
            user.lastname = data.lastname

        if data.country_code:
            validate_country_code(data.country_code)
            user.country_code = data.country_code

        if data.phone_number:
            validate_phone_number(data.phone_number)

            # Verifica si otro usuario ya tiene este teléfono
            result = await db.execute(
                select(User).where(
                    User.country_code == user.country_code,
                    User.phone_number == data.phone_number,
                    User.id != user.id
                )
            )
            existing_user = result.scalar_one_or_none()
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Phone number is already registered by another user."
                )

            user.phone_number = data.phone_number

        if data.password:
            validate_password_strength(data.password)
            user.password = hash_password(data.password)

        if data.profile_photo:
            data.profile_photo.file.seek(0)  # 🔁 asegura que está en posición inicial
            validated = validate_profile_photo(data.profile_photo)
            user.profile_photo = validated
            logger.debug(f"📸 Foto subida — tamaño: {len(validated)} bytes")

        # Actualizar el usuario en la base de datos
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"🔄 Updated profile for user {user.email}")

        # ✅ Retornar un dict compatible con el response_model
        return {
            "id": user.id,
            "name": user.name,
            "lastname": user.lastname,
            "email": user.email,
            "nickname": user.nickname,
            "phone_number": user.phone_number,
            "country": user.country,
            "country_code": user.country_code,
            "profile_photo_url": f"/profile/photo/{user.id}" if user.profile_photo else None
        }
