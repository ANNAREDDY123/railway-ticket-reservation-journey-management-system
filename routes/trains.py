from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.train import Train
from schemas.train import TrainCreate

router = APIRouter(
    prefix="/trains",
    tags=["Trains"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_train(
    train: TrainCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Train).filter(
        Train.train_number == train.train_number
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Train number already exists."
        )

    db_train = Train(**train.dict())

    db.add(db_train)
    db.commit()
    db.refresh(db_train)

    return db_train


@router.get("/")
def get_trains(
    source: str = None,
    destination: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Train)

    if source:
        query = query.filter(
            Train.source.contains(source)
        )

    if destination:
        query = query.filter(
            Train.destination.contains(destination)
        )

    total = query.count()

    trains = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": trains
    }


@router.get("/{train_id}")
def get_train(
    train_id: int,
    db: Session = Depends(get_db)
):

    train = db.query(Train).filter(
        Train.id == train_id
    ).first()

    if not train:

        raise HTTPException(
            status_code=404,
            detail="Train not found."
        )

    return train


@router.put("/{train_id}")
def update_train(
    train_id: int,
    train: TrainCreate,
    db: Session = Depends(get_db)
):

    db_train = db.query(Train).filter(
        Train.id == train_id
    ).first()

    if not db_train:

        raise HTTPException(
            status_code=404,
            detail="Train not found."
        )

    db_train.train_number = train.train_number
    db_train.train_name = train.train_name
    db_train.source = train.source
    db_train.destination = train.destination
    db_train.total_seats = train.total_seats

    db.commit()

    return {
        "message": "Train updated successfully."
    }


@router.delete("/{train_id}")
def delete_train(
    train_id: int,
    db: Session = Depends(get_db)
):

    train = db.query(Train).filter(
        Train.id == train_id
    ).first()

    if not train:

        raise HTTPException(
            status_code=404,
            detail="Train not found."
        )

    db.delete(train)

    db.commit()

    return {
        "message": "Train deleted successfully."
    }
