import pytest
from src.entities.event import Event, EventCategory
from src.entities.ticket import Ticket, TicketStatus
from src.interface_adapters.repositories.in_memory_event_repository import InMemoryEventRepository
from src.interface_adapters.repositories.in_memory_ticket_repository import InMemoryTicketRepository

from src.use_cases.list_events import ListEventsInput, ListEventsUseCase
from src.use_cases.buy_ticket import BuyTicketInput, BuyTicketUseCase
from src.use_cases.list_purchased_tickets import ListPurchasedTicketsInput, ListPurchasedTicketsUseCase
from src.use_cases.cancel_ticket import CancelTicketInput, CancelTicketUseCase
from src.use_cases.validate_ticket import ValidateTicketInput, ValidateTicketUseCase
from src.use_cases.get_event import GetEventInput, GetEventUseCase

@pytest.fixture
def setup_repos():
    event_repo = InMemoryEventRepository()
    ticket_repo = InMemoryTicketRepository()
    
    # Seed event
    event = Event(
        id="test-evt",
        title="Live Concert",
        description="Music event",
        categories={
            "VIP": EventCategory(name="VIP", price=100.0, total_capacity=2, available_seats=2),
            "Regular": EventCategory(name="Regular", price=50.0, total_capacity=10, available_seats=10)
        }
    )
    event_repo.save(event)
    return event_repo, ticket_repo

def test_list_events(setup_repos):
    event_repo, _ = setup_repos
    use_case = ListEventsUseCase(event_repo)
    output = use_case.execute(ListEventsInput())
    
    assert output.total == 1
    assert output.events[0].title == "Live Concert"

def test_buy_ticket_success(setup_repos):
    event_repo, ticket_repo = setup_repos
    use_case = BuyTicketUseCase(event_repo, ticket_repo)
    
    output = use_case.execute(BuyTicketInput(
        event_id="test-evt",
        category_name="VIP",
        purchaser_email="buyer@test.com"
    ))
    
    assert output.success is True
    assert output.ticket is not None
    assert output.ticket.price == 100.0
    assert output.ticket.status == TicketStatus.ACTIVE
    
    # Check that stock was reduced
    event = event_repo.find_by_id("test-evt")
    assert event.categories["VIP"].available_seats == 1

def test_buy_ticket_out_of_stock(setup_repos):
    event_repo, ticket_repo = setup_repos
    use_case = BuyTicketUseCase(event_repo, ticket_repo)
    
    # Book all VIP seats
    use_case.execute(BuyTicketInput("test-evt", "VIP", "b1@test.com"))
    use_case.execute(BuyTicketInput("test-evt", "VIP", "b2@test.com"))
    
    # Next booking should fail
    output = use_case.execute(BuyTicketInput("test-evt", "VIP", "b3@test.com"))
    assert output.success is False
    assert "No tickets available" in output.message

def test_list_purchased_tickets(setup_repos):
    event_repo, ticket_repo = setup_repos
    buy_use_case = BuyTicketUseCase(event_repo, ticket_repo)
    list_use_case = ListPurchasedTicketsUseCase(ticket_repo)
    
    buy_use_case.execute(BuyTicketInput("test-evt", "VIP", "client@test.com"))
    buy_use_case.execute(BuyTicketInput("test-evt", "Regular", "client@test.com"))
    buy_use_case.execute(BuyTicketInput("test-evt", "Regular", "other@test.com"))
    
    output = list_use_case.execute(ListPurchasedTicketsInput(purchaser_email="client@test.com"))
    assert output.success is True
    assert len(output.tickets) == 2

def test_cancel_ticket_success(setup_repos):
    event_repo, ticket_repo = setup_repos
    buy_use_case = BuyTicketUseCase(event_repo, ticket_repo)
    cancel_use_case = CancelTicketUseCase(event_repo, ticket_repo)
    
    buy_output = buy_use_case.execute(BuyTicketInput("test-evt", "VIP", "client@test.com"))
    ticket_id = buy_output.ticket.id
    
    # VIP stock should be 1
    event = event_repo.find_by_id("test-evt")
    assert event.categories["VIP"].available_seats == 1
    
    # Cancel ticket
    cancel_output = cancel_use_case.execute(CancelTicketInput(
        ticket_id=ticket_id,
        purchaser_email="client@test.com"
    ))
    
    assert cancel_output.success is True
    assert cancel_output.ticket.status == TicketStatus.CANCELLED
    
    # VIP stock should be returned to 2
    event = event_repo.find_by_id("test-evt")
    assert event.categories["VIP"].available_seats == 2

def test_cancel_ticket_unauthorized(setup_repos):
    event_repo, ticket_repo = setup_repos
    buy_use_case = BuyTicketUseCase(event_repo, ticket_repo)
    cancel_use_case = CancelTicketUseCase(event_repo, ticket_repo)
    
    buy_output = buy_use_case.execute(BuyTicketInput("test-evt", "VIP", "client@test.com"))
    ticket_id = buy_output.ticket.id
    
    # Try cancelling with wrong email
    cancel_output = cancel_use_case.execute(CancelTicketInput(
        ticket_id=ticket_id,
        purchaser_email="hacker@test.com"
    ))
    
    assert cancel_output.success is False
    assert "Unauthorized" in cancel_output.message

def test_validate_ticket(setup_repos):
    event_repo, ticket_repo = setup_repos
    buy_use_case = BuyTicketUseCase(event_repo, ticket_repo)
    validate_use_case = ValidateTicketUseCase(ticket_repo)
    
    buy_output = buy_use_case.execute(BuyTicketInput("test-evt", "VIP", "client@test.com"))
    ticket_id = buy_output.ticket.id
    
    # Validate ticket at gate
    val_output = validate_use_case.execute(ValidateTicketInput(ticket_id=ticket_id))
    assert val_output.success is True
    assert val_output.ticket.status == TicketStatus.USED
    
    # Validate again should fail
    val_output2 = validate_use_case.execute(ValidateTicketInput(ticket_id=ticket_id))
    assert val_output2.success is False
    assert "already been used" in val_output2.message

def test_get_event(setup_repos):
    event_repo, _ = setup_repos
    use_case = GetEventUseCase(event_repo)
    
    # Successful fetch by exact ID
    output = use_case.execute(GetEventInput(event_id="test-evt"))
    assert output.success is True
    assert output.event.title == "Live Concert"

    # Successful fetch by prefix
    output_prefix = use_case.execute(GetEventInput(event_id="test-e"))
    assert output_prefix.success is True
    assert output_prefix.event.title == "Live Concert"

    # Event not found
    output_not_found = use_case.execute(GetEventInput(event_id="non-existent"))
    assert output_not_found.success is False
    assert "not found" in output_not_found.message
