from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy import select, update
from src.models.login_attempt_model import LoginAttempt

MAX_ATTEMPTS = 3
LOCK_MINUTES = 15

# ⛔ Verifica si debe bloquear el intento
async def check_login_attempts(db, user_id: int):
    result = await db.execute(select(LoginAttempt).where(LoginAttempt.user_id == user_id))
    attempt = result.scalar_one_or_none()

    if attempt and attempt.failed_attempts >= MAX_ATTEMPTS:
        if attempt.last_failed_at and datetime.utcnow() - attempt.last_failed_at < timedelta(minutes=LOCK_MINUTES):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed login attempts. Try again in 15 minutes."
            )

# ✅ Resetea los intentos al login exitoso
async def reset_login_attempts(db, user_id: int):
    await db.execute(
        update(LoginAttempt)
        .where(LoginAttempt.user_id == user_id)
        .values(failed_attempts=0, last_failed_at=None)
    )
    await db.commit()

# 🔁 Suma intento fallido o crea el registro
async def increment_login_attempts(db, user_id: int):
    result = await db.execute(select(LoginAttempt).where(LoginAttempt.user_id == user_id))
    attempt = result.scalar_one_or_none()

    if attempt:
        await db.execute(
            update(LoginAttempt)
            .where(LoginAttempt.user_id == user_id)
            .values(
                failed_attempts=attempt.failed_attempts + 1,
                last_failed_at=datetime.utcnow()
            )
        )
    else:
        db.add(LoginAttempt(user_id=user_id, failed_attempts=1, last_failed_at=datetime.utcnow()))

    await db.commit()
