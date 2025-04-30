from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class MovieCreateRequest(BaseModel):
    title: str = Field(..., example="Inception")
    description: Optional[str] = Field(None, example="A mind-bending thriller.")
    poster_url: Optional[HttpUrl] = Field(None, example="https://example.com/inception.jpg")
    year: Optional[int] = Field(None, ge=1800, le=2100, example=2010)
    duration_minutes: Optional[int] = Field(None, ge=1, le=600, example=148)
    director: Optional[str] = Field(None, example="Christopher Nolan")
    genre_ids: List[int] = Field(..., example=[1, 2])

class MovieUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, example="Inception Updated")
    description: Optional[str] = Field(None)
    poster_url: Optional[HttpUrl] = Field(None)
    year: Optional[int] = Field(None, ge=1800, le=2100)
    duration_minutes: Optional[int] = Field(None, ge=1, le=600)
    director: Optional[str] = Field(None)
    genre_ids: Optional[List[int]] = Field(None)
