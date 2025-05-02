from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ShowtimeCreateRequest(BaseModel):
    movie_id: int
    show_datetime: datetime

class ShowtimeUpdateRequest(BaseModel):
    show_datetime: Optional[datetime] = None

class ShowtimeCreateRequest(BaseModel):
    movie_id: int
    show_datetime: Optional[datetime] = None