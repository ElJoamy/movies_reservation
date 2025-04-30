import re
import os
import imghdr
from fastapi import UploadFile, HTTPException
from src.utils.logger import setup_logger
from src.config.config import get_settings

_SETTINGS = get_settings()
logger = setup_logger(__name__, level=_SETTINGS.log_level)

# 📁 Ruta del archivo con dominios de correo no permitidos
INVALID_DOMAINS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "docs",
    "helpers",
    "invalid_email_domains.txt"
)
# 🔁 Carga los dominios al iniciar
with open(INVALID_DOMAINS_FILE, "r", encoding="utf-8") as f:
    INVALID_EMAIL_DOMAINS = set(line.strip().lower() for line in f if line.strip())

logger.info(f"✅ Loaded {len(INVALID_EMAIL_DOMAINS)} invalid email domains")

def validate_email_domain(email: str) -> str:
    if "@" not in email:
        logger.warning("❌ Email missing '@': %s", email)
        raise HTTPException(status_code=400, detail="Invalid email format.")
    domain = email.split('@')[-1].lower()
    if domain in INVALID_EMAIL_DOMAINS:
        logger.warning("❌ Email domain is disposable: %s", domain)
        raise HTTPException(status_code=400, detail="Disposable or temporary email addresses are not allowed.")
    return email

def validate_country_code(value: str) -> str:
    if not re.match(r'^\+\d{1,4}$', value):
        logger.warning("❌ Invalid country code: %s", value)
        raise HTTPException(
            status_code=400,
            detail="Country code must start with '+' followed by 1 to 4 digits (e.g., +591, +1)"
        )
    return value

def validate_phone_number(value: str) -> str:
    if not re.match(r'^\d{6,15}$', value):
        logger.warning("❌ Invalid phone number: %s", value)
        raise HTTPException(
            status_code=400,
            detail="Phone number must be between 6 and 15 digits, without spaces or symbols."
        )
    return value

def validate_password_strength(value: str) -> str:
    if len(value) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', value):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', value):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
    if not re.search(r'\d', value):
        raise HTTPException(status_code=400, detail="Password must contain at least one number.")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>-]', value):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character.")

    digits = re.findall(r'\d+', value)
    for group in digits:
        if len(group) >= 3 and (is_sequential(group) or is_sequential(group[::-1])):
            raise HTTPException(status_code=400, detail="Password must not contain sequential digits (e.g., 123 or 987).")

    return value

def is_sequential(digits: str) -> bool:
    return all(int(digits[i]) + 1 == int(digits[i + 1]) for i in range(len(digits) - 1))

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".heif"}
ALLOWED_IMAGE_MIME_TYPES = {"image/jpeg", "image/png", "image/heic", "image/heif"}
MAX_IMAGE_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB

def validate_profile_photo(file: UploadFile) -> bytes:
    filename = file.filename.lower()

    if ".." in filename or "/" in filename or "\\" in filename:
        logger.warning("❌ Path traversal attempt in filename: %s", filename)
        raise HTTPException(status_code=400, detail="Invalid filename.")

    if not any(filename.endswith(ext) for ext in ALLOWED_IMAGE_EXTENSIONS):
        logger.warning("❌ Invalid image extension: %s", filename)
        raise HTTPException(status_code=400, detail="Only JPG, JPEG, PNG, HEIC or HEIF images are allowed.")

    if file.content_type not in ALLOWED_IMAGE_MIME_TYPES:
        logger.warning("❌ Invalid MIME type: %s", file.content_type)
        raise HTTPException(status_code=400, detail="Unsupported image content type.")

    content = file.file.read()

    if len(content) > MAX_IMAGE_SIZE_BYTES:
        logger.warning("❌ Image size exceeds 2MB: %d bytes", len(content))
        raise HTTPException(status_code=400, detail="Image file exceeds the 2MB size limit.")

    real_type = imghdr.what(None, h=content)
    if real_type not in {"jpeg", "png", "heic", "heif"}:
        logger.warning("❌ Invalid image content detected: %s", real_type)
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

    logger.info("✅ Image validated: %s (%s)", filename, real_type)
    return content
