import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routes.auth import router as auth_router
from routes.trains import router as trains_router
from routes.bookings import router as bookings_router
from routes.journey import router as journey_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Railway Ticket Reservation & Journey Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(trains_router)
app.include_router(bookings_router)
app.include_router(journey_router)


@app.get("/")
def home():

    logger.info("Application Started Successfully")

    return {
        "message": "Railway Ticket Reservation & Journey Management System"
    }
