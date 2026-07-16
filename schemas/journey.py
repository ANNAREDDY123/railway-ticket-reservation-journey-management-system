from pydantic import BaseModel


class JourneyCreate(BaseModel):

    booking_id: int
