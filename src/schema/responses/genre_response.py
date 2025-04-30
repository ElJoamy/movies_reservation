from pydantic import BaseModel

class GenreResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True