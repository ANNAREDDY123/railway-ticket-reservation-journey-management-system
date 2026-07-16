CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE trains(
    id INTEGER PRIMARY KEY,
    train_number VARCHAR(50) UNIQUE,
    train_name VARCHAR(100),
    source VARCHAR(100),
    destination VARCHAR(100),
    total_seats INTEGER
);

CREATE TABLE bookings(
    id INTEGER PRIMARY KEY,
    passenger_id INTEGER,
    train_id INTEGER,
    journey_date DATE,
    seat_number INTEGER,
    ticket_status VARCHAR(50)
);

CREATE TABLE journeys(
    id INTEGER PRIMARY KEY,
    booking_id INTEGER,
    journey_status VARCHAR(50),
    started_at DATETIME,
    completed_at DATETIME
);
