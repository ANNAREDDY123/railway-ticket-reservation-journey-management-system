from pydantic import (
    BaseModel,
    Field
)


class TrainCreate(BaseModel):

    train_number: str = Field(..., min_length=3)

    train_name: str = Field(..., min_length=3)

    source: str = Field(..., min_length=3)

    destination: str = Field(..., min_length=3)

    total_seats: int = Field(..., gt=0)
