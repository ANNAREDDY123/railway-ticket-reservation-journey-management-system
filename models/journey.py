from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from database import Base


class Journey(Base):

    __tablename__ = "journeys"

    id = Column(
        Integer,
        primary_key=True
    )

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id")
    )

    journey_status = Column(String)

    started_at = Column(DateTime)

    completed_at = Column(DateTime)
