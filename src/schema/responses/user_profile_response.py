from pydantic import BaseModel
from typing import Optional

class UserProfileResponse(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    nickname: str
    phone_number: str
    country: str
    country_code: str
    profile_photo_url: Optional[str]

    class Config:
        orm_mode = True
