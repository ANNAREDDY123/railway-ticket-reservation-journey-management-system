from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from datetime import datetime

from database import SessionLocal

from models.journey import Journey
from models.booking import Booking

from schemas.journey import JourneyCreate

router = APIRouter(
    prefix="/journey",
    tags=["Journey"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/start")
def start_journey(
    journey: JourneyCreate,
    db: Session = Depends(get_db)
):

    booking = db.query(Booking).filter(
        Booking.id == journey.booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )

    new_journey = Journey(
        booking_id=journey.booking_id,
        journey_status="Started",
        started_at=datetime.now()
    )

    db.add(new_journey)
    db.commit()

    return {
        "message": "Journey started successfully."
    }


@router.post("/complete")
def complete_journey(
    journey: JourneyCreate,
    db: Session = Depends(get_db)
):

    db_journey = db.query(Journey).filter(
        Journey.booking_id == journey.booking_id
    ).first()

    if not db_journey:

        raise HTTPException(
            status_code=404,
            detail="Journey not found."
        )

    db_journey.journey_status = "Completed"
    db_journey.completed_at = datetime.now()

    db.commit()

    return {
        "message": "Journey completed successfully."
    }


@router.get("/passengers/{passenger_id}/journeys")
def passenger_history(
    passenger_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Journey).join(
        Booking,
        Journey.booking_id == Booking.id
    ).filter(
        Booking.passenger_id == passenger_id
    ).all()
