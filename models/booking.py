from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey
)

from database import Base


class Booking(Base):

    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True
    )

    passenger_id = Column(Integer)

    train_id = Column(
        Integer,
        ForeignKey("trains.id")
    )

    journey_date = Column(Date)

    seat_number = Column(Integer)

    ticket_status = Column(String)
