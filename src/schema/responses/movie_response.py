from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class GenreResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ShowtimeResponse(BaseModel):
    id: int
    show_datetime: datetime

    class Config:
        orm_mode = True

class MovieResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    poster_url: Optional[HttpUrl]
    year: Optional[int]
    duration_minutes: Optional[int]
    director: Optional[str]
    genres: List[GenreResponse]

    class Config:
        orm_mode = True

class MovieWithShowtimesResponse(MovieResponse):
    showtimes: List[ShowtimeResponse]