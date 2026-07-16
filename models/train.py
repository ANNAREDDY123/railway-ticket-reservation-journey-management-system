from sqlalchemy import (
    Column,
    Integer,
    String
)

from database import Base


class Train(Base):

    __tablename__ = "trains"

    id = Column(
        Integer,
        primary_key=True
    )

    train_number = Column(
        String,
        unique=True
    )

    train_name = Column(String)

    source = Column(String)

    destination = Column(String)

    total_seats = Column(Integer)
