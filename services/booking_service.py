from datetime import date


def valid_ticket_status(status):

    return status in [
        "Booked",
        "Confirmed",
        "Waiting List",
        "Cancelled"
    ]


def valid_journey_date(journey_date):

    return journey_date >= date.today()


def seat_available(existing_booking):

    return existing_booking is None
