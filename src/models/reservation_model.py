from sqlalchemy import ForeignKey, TIMESTAMP, text, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base

class Reservation(Base):
    __tablename__ = "reservation"
    __table_args__ = (
        UniqueConstraint('seat_id', name='unique_seat_reservation'),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(INTEGER, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    showtime_id: Mapped[int] = mapped_column(INTEGER, ForeignKey("showtime.id", ondelete="CASCADE"), nullable=False)
    seat_id: Mapped[int] = mapped_column(INTEGER, ForeignKey("seat.id", ondelete="CASCADE"), nullable=False)
    reserved_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship("User", backref="reservations")
    showtime = relationship("Showtime", backref="reservations")
    seat = relationship("Seat", back_populates="reservation")
