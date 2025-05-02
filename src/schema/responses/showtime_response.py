from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BasicMovieResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    poster_url: Optional[str]
    duration_minutes: Optional[int]
    director: Optional[str]

    class Config:
        from_attributes = True 

class SeatResponse(BaseModel):
    id: int
    seat_number: str
    is_reserved: bool

    class Config:
        from_attributes = True

class ShowtimeDetailResponse(BaseModel):
    id: int
    show_datetime: datetime
    movie: BasicMovieResponse
    seats: List[SeatResponse]

    class Config:
        from_attributes = True

class ShowtimeBriefResponse(BaseModel):
    id: int
    show_datetime: datetime

    class Config:
        from_attributes = True

class MovieWithShowtimesGroupedResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    poster_url: Optional[str]
    duration_minutes: Optional[int]
    director: Optional[str]
    showtimes: List[ShowtimeBriefResponse]

    class Config:
        from_attributes = True
