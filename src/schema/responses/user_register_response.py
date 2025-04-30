from pydantic import BaseModel, EmailStr

class UserRegisterResponse(BaseModel):
    id: int
    name: str
    lastname: str
    nickname: str
    email: EmailStr
    country_code: str
    phone_number: str
    country: str
