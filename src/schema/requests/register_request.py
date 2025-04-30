from pydantic import BaseModel, Field, validator, EmailStr
import re

class RegisterRequest(BaseModel):
    name: str
    lastname: str
    nickname: str
    email: EmailStr
    password: str
    country_code: str
    phone_number: str
    country: str

    @validator("country_code")
    def validate_country_code(cls, value):
        # Validar que empiece con "+" seguido de 1 a 4 dígitos
        if not re.match(r'^\+\d{1,4}$', value):
            raise ValueError("Country code must start with '+' followed by 1 to 4 digits (e.g., +591, +1)")
        return value

    @validator("phone_number")
    def validate_phone_number(cls, value):
        # Aceptar entre 6 y 15 dígitos sin símbolos
        if not re.match(r'^\d{6,15}$', value):
            raise ValueError("Phone number must be between 6 and 15 digits, without spaces or symbols")
        return value

    @validator("password")
    def validate_password_strength(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>-]', value):
            raise ValueError("Password must contain at least one special character")

        # Bloquear secuencias numéricas como 123, 456, 789, 012, 321, 987, etc.
        digits = re.findall(r'\d+', value)
        for group in digits:
            if len(group) >= 3 and (cls.is_sequential(group) or cls.is_sequential(group[::-1])):
                raise ValueError("Password must not contain 3 or more sequential numbers (e.g., 123, 789)")

        return value

    @staticmethod
    def is_sequential(digits: str) -> bool:
        return all(int(digits[i]) + 1 == int(digits[i+1]) for i in range(len(digits) - 1))
