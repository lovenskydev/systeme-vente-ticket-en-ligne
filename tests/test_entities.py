import pytest
from datetime import datetime, timezone
from src.entities.event import Event, EventCategory
from src.entities.ticket import Ticket, TicketStatus

def test_event_category_validation():
    # Valid category
    cat = EventCategory(name="VIP", price=100.0, total_capacity=10, available_seats=10)
    assert cat.name == "VIP"
    assert cat.price == 100.0
    assert cat.total_capacity == 10
    assert cat.available_seats == 10

    # Negative price
    with pytest.raises(ValueError, match="Price cannot be negative"):
        EventCategory(name="VIP", price=-10.0, total_capacity=10, available_seats=10)

    # Negative capacity
    with pytest.raises(ValueError, match="Total capacity cannot be negative"):
        EventCategory(name="VIP", price=100.0, total_capacity=-5, available_seats=10)

    # Seats exceed capacity
    with pytest.raises(ValueError, match="Available seats cannot exceed total capacity"):
        EventCategory(name="VIP", price=100.0, total_capacity=10, available_seats=15)

def test_event_creation():
    categories = {
        "VIP": EventCategory(name="VIP", price=150.0, total_capacity=5, available_seats=5)
    }
    event = Event(title="Rock Concert", description="Classic Rock", categories=categories)
    assert event.title == "Rock Concert"
    assert "VIP" in event.categories

    # Empty title
    with pytest.raises(ValueError, match="Event title cannot be empty"):
        Event(title="   ", categories=categories)

    # No categories
    with pytest.raises(ValueError, match="Event must have at least one ticket category"):
        Event(title="No Cat Event", categories={})

def test_event_booking_and_releasing():
    cat = EventCategory(name="Regular", price=50.0, total_capacity=2, available_seats=2)
    event = Event(title="Match", categories={"Regular": cat})

    # Book 1 ticket
    event.book_ticket("Regular")
    assert event.categories["Regular"].available_seats == 1

    # Book 2nd ticket
    event.book_ticket("Regular")
    assert event.categories["Regular"].available_seats == 0

    # Book 3rd ticket (should fail)
    with pytest.raises(ValueError, match="No tickets available for category"):
        event.book_ticket("Regular")

    # Release 1 ticket
    event.release_ticket("Regular")
    assert event.categories["Regular"].available_seats == 1

    # Release 2nd ticket
    event.release_ticket("Regular")
    assert event.categories["Regular"].available_seats == 2

    # Release 3rd ticket (should exceed capacity and fail)
    with pytest.raises(ValueError, match="already at full capacity"):
        event.release_ticket("Regular")

def test_ticket_creation():
    ticket = Ticket(
        event_id="evt-1",
        event_name="Art Expo",
        category_name="General",
        price=20.0,
        purchaser_email="user@test.com"
    )
    assert ticket.status == TicketStatus.ACTIVE
    assert ticket.purchaser_email == "user@test.com"

    # Invalid email
    with pytest.raises(ValueError, match="Invalid purchaser email format"):
        Ticket(
            event_id="evt-1",
            event_name="Art Expo",
            category_name="General",
            price=20.0,
            purchaser_email="invalidemail"
        )

def test_ticket_cancellation():
    ticket = Ticket(
        event_id="evt-1",
        event_name="Art Expo",
        category_name="General",
        price=20.0,
        purchaser_email="user@test.com"
    )
    ticket.cancel()
    assert ticket.status == TicketStatus.CANCELLED

    # Re-cancellation should fail
    with pytest.raises(ValueError, match="Ticket is already cancelled"):
        ticket.cancel()

def test_ticket_validation():
    ticket = Ticket(
        event_id="evt-1",
        event_name="Art Expo",
        category_name="General",
        price=20.0,
        purchaser_email="user@test.com"
    )
    ticket.validate()
    assert ticket.status == TicketStatus.USED

    # Validation on used ticket fails
    with pytest.raises(ValueError, match="Ticket has already been used"):
        ticket.validate()

    # Cancellation on used ticket fails
    with pytest.raises(ValueError, match="Cannot cancel a ticket that has already been used"):
        ticket.cancel()
