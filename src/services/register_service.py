from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user_model import User
from src.schema.requests.register_request import RegisterRequest
from src.utils.password_handler import hash_password
from src.utils.logger import setup_logger
from src.config.config import get_settings
from src.utils.validators import (
    validate_email_domain,
    validate_country_code,
    validate_phone_number,
    validate_password_strength,
)

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

class RegisterService:
    async def register_user(self, db: AsyncSession, register_data: RegisterRequest):
        logger.info(f"🔐 Register attempt for email: {register_data.email}")

        # ✅ Validaciones previas
        validate_email_domain(register_data.email)
        validate_country_code(register_data.country_code)
        validate_phone_number(register_data.phone_number)
        validate_password_strength(register_data.password)

        # ❌ Email ya registrado
        result_email = await db.execute(select(User).where(User.email == register_data.email))
        if result_email.scalar_one_or_none():
            logger.warning(f"❌ Email already registered: {register_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered."
            )

        # ❌ Teléfono ya registrado
        result_phone = await db.execute(
            select(User).where(
                User.country_code == register_data.country_code,
                User.phone_number == register_data.phone_number
            )
        )
        if result_phone.scalar_one_or_none():
            logger.warning(f"❌ Phone number already registered: {register_data.country_code}{register_data.phone_number}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number is already registered."
            )

        # ✅ Crear usuario
        try:
            new_user = User(
                name=register_data.name,
                lastname=register_data.lastname,
                nickname=register_data.nickname,
                email=register_data.email,
                password=hash_password(register_data.password),
                country_code=register_data.country_code,
                phone_number=register_data.phone_number,
                country=register_data.country
            )

            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            logger.info(f"✅ User registered successfully: id={new_user.id}, email={new_user.email}")
            return {
                "id": new_user.id,
                "name": new_user.name,
                "lastname": new_user.lastname,
                "nickname": new_user.nickname,
                "email": new_user.email,
                "country_code": new_user.country_code,
                "phone_number": new_user.phone_number,
                "country": new_user.country
            }
        except Exception as e:
            logger.error(f"❌ Error creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during registration."
            )
