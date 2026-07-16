from pydantic import (
    BaseModel,
    Field
)

from datetime import date


class BookingCreate(BaseModel):

    passenger_id: int

    train_id: int

    journey_date: date

    seat_number: int = Field(..., gt=0)

    ticket_status: str
