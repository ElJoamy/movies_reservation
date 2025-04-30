from sqlalchemy import ForeignKey, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base
from src.models.reservation_model import Reservation

class Seat(Base):
    __tablename__ = "seat"
    __table_args__ = (
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    showtime_id: Mapped[int] = mapped_column(INTEGER, ForeignKey("showtime.id", ondelete="CASCADE"), nullable=False)
    seat_number: Mapped[str] = mapped_column(String(10), nullable=False)
    is_reserved: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    showtime = relationship("Showtime", back_populates="seats")
    reservation = relationship("Reservation", back_populates="seat", uselist=False)
