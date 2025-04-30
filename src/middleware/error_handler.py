from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from src.config.config import get_settings
from src.utils.logger import setup_logger
import traceback

_SETTINGS = get_settings()

logger = setup_logger(__name__, level=_SETTINGS.log_level)

async def global_exception_handler(request: Request, exc: Exception):
    """
    Global handler for uncaught exceptions.
    Returns detailed trace in DEBUG mode, and a generic error in production.
    """
    trace = traceback.format_exc()
    logger.error(f"🔥 Unhandled exception:\n{trace}")

    if _SETTINGS.debug:
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": str(exc),
                "type": exc.__class__.__name__,
                "trace": trace
            }
        )
    else:
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal Server Error. Please try again later."
            }
        )
