from pydantic import BaseModel

class TokenResponse(BaseModel):
    message: str
    jti: str  # ID único del access_token