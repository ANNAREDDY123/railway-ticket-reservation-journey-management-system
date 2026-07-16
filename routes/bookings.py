from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal

from models.booking import Booking
from models.train import Train

from schemas.booking import BookingCreate

from services.booking_service import (
    valid_ticket_status,
    valid_journey_date,
    seat_available
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):

    train = db.query(Train).filter(
        Train.id == booking.train_id
    ).first()

    if not train:

        raise HTTPException(
            status_code=404,
            detail="Train not found."
        )

    if not valid_journey_date(
        booking.journey_date
    ):

        raise HTTPException(
            status_code=400,
            detail="Journey date cannot be in the past."
        )

    existing = db.query(Booking).filter(
        Booking.train_id == booking.train_id,
        Booking.journey_date == booking.journey_date,
        Booking.seat_number == booking.seat_number,
        Booking.ticket_status != "Cancelled"
    ).first()

    if not seat_available(existing):

        raise HTTPException(
            status_code=400,
            detail="Seat already booked."
        )

    booked = db.query(Booking).filter(
        Booking.train_id == booking.train_id,
        Booking.journey_date == booking.journey_date,
        Booking.ticket_status != "Cancelled"
    ).count()

    status = booking.ticket_status

    if booked >= train.total_seats:
        status = "Waiting List"

    db_booking = Booking(
        passenger_id=booking.passenger_id,
        train_id=booking.train_id,
        journey_date=booking.journey_date,
        seat_number=booking.seat_number,
        ticket_status=status
    )

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    return db_booking


@router.get("/")
def get_bookings(
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Booking)

    if status:

        query = query.filter(
            Booking.ticket_status == status
        )

    total = query.count()

    bookings = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": bookings
    }


@router.get("/{booking_id}")
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )

    return booking


@router.put("/{booking_id}")
def update_booking(
    booking_id: int,
    booking: BookingCreate,
    db: Session = Depends(get_db)
):

    db_booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not db_booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )

    db_booking.ticket_status = booking.ticket_status

    db.commit()

    return {
        "message": "Booking updated successfully."
    }


@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )

    booking.ticket_status = "Cancelled"

    waiting = db.query(Booking).filter(
        Booking.train_id == booking.train_id,
        Booking.journey_date == booking.journey_date,
        Booking.ticket_status == "Waiting List"
    ).first()

    if waiting:

        waiting.ticket_status = "Confirmed"

    db.commit()

    return {
        "message": "Ticket cancelled successfully."
    }
