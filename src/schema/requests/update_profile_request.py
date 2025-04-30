from fastapi import Form, File, UploadFile
from typing import Optional, Union

class UpdateProfileRequest:
    def __init__(
        self,
        name: Optional[str] = Form(None),
        lastname: Optional[str] = Form(None),
        country_code: Optional[str] = Form(None),
        phone_number: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        profile_photo: Optional[UploadFile] = File(None)
    ):
        self.name = name
        self.lastname = lastname
        self.country_code = country_code
        self.phone_number = phone_number
        self.password = password
        self.profile_photo = profile_photo  # ✅ deja el UploadFile intacto
