# railway-ticket-reservation-journey-management-system
FastAPI Railway Ticket Reservation &amp; Journey Management System with JWT Authentication, Train Management, Ticket Booking, Journey Management, Reports, Search, SQLAlchemy ORM, Pagination, Logging, Docker Support, and Unit Tests.
# Railway Ticket Reservation & Journey Management System

## Features

- JWT Authentication
- Train Management (CRUD)
- Ticket Booking
- Journey Management
- Reports & Search
- SQLAlchemy ORM
- SQLite Database
- Docker Support
- Logging
- Basic Unit Tests


## Setup Instructions

### Install Dependencies


pip install -r requirements.txt


### Run Project


py -m uvicorn main:app --reload


Swagger


http://127.0.0.1:8000/docs


## Environment Variables


SECRET_KEY=railway_secret_key
ALGORITHM=HS256


## API Examples

- POST `/auth/register`
- POST `/auth/login`
- POST `/trains`
- POST `/bookings`
- POST `/journey/start`
- POST `/journey/complete`



## Docker Deployment


docker build -t railway-system .
docker run -p 8000:8000 railway-system


## Assumptions

- Train number must be unique.
- Journey date cannot be in the past.
- Seat numbers cannot be duplicated for the same train and journey date.
- Waiting List is assigned automatically when seats are full.
- Cancelled tickets release seats for waiting passengers.
