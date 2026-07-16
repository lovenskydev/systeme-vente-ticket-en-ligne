from dataclasses import dataclass
from src.entities.ticket import Ticket
from src.use_cases.interfaces.event_repository import EventRepository
from src.use_cases.interfaces.ticket_repository import TicketRepository

@dataclass
class BuyTicketInput:
    event_id: str
    category_name: str
    purchaser_email: str

@dataclass
class BuyTicketOutput:
    ticket: Ticket | None
    success: bool
    message: str

class BuyTicketUseCase:
    def __init__(self, event_repository: EventRepository, ticket_repository: TicketRepository) -> None:
        self.event_repository = event_repository
        self.ticket_repository = ticket_repository

    def execute(self, input_data: BuyTicketInput) -> BuyTicketOutput:
        # Step 1: Retrieve the event
        event = self.event_repository.find_by_id(input_data.event_id)
        if not event:
            return BuyTicketOutput(ticket=None, success=False, message=f"Event '{input_data.event_id}' not found")

        # Step 2: Book seat on the Event entity (validates category existence and stock)
        try:
            event.book_ticket(input_data.category_name)
        except ValueError as exc:
            return BuyTicketOutput(ticket=None, success=False, message=str(exc))

        # Step 3: Create the Ticket entity (validates fields like email format)
        try:
            category = event.categories[input_data.category_name]
            ticket = Ticket(
                event_id=event.id,
                event_name=event.title,
                category_name=input_data.category_name,
                price=category.price,
                purchaser_email=input_data.purchaser_email
            )
        except ValueError as exc:
            # Revert in-memory event mutation (optional but clean for testing)
            event.release_ticket(input_data.category_name)
            return BuyTicketOutput(ticket=None, success=False, message=str(exc))

        # Step 4: Persist the updated Event and the new Ticket
        self.event_repository.update(event)
        saved_ticket = self.ticket_repository.save(ticket)

        return BuyTicketOutput(
            ticket=saved_ticket,
            success=True,
            message=f"Ticket successfully purchased! Ticket Code: {saved_ticket.id}"
        )
