from fastapi import Form, File, UploadFile
from typing import Optional
from src.schema.requests.update_profile_request import UpdateProfileRequest

def get_update_profile_data(
    name: Optional[str] = Form(None),
    lastname: Optional[str] = Form(None),
    country_code: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    profile_photo: Optional[UploadFile] = File(None),
) -> UpdateProfileRequest:
    return UpdateProfileRequest(
        name=name,
        lastname=lastname,
        country_code=country_code,
        phone_number=phone_number,
        password=password,
        profile_photo=profile_photo,
    )
