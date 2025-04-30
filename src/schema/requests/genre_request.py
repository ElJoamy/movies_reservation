from pydantic import BaseModel

class GenreCreateRequest(BaseModel):
    name: str

class GenreUpdateRequest(BaseModel):
    name: str