from dataclasses import dataclass
from src.entities.ticket import Ticket
from src.use_cases.interfaces.event_repository import EventRepository
from src.use_cases.interfaces.ticket_repository import TicketRepository

@dataclass
class CancelTicketInput:
    ticket_id: str
    purchaser_email: str

@dataclass
class CancelTicketOutput:
    ticket: Ticket | None
    success: bool
    message: str

class CancelTicketUseCase:
    def __init__(self, event_repository: EventRepository, ticket_repository: TicketRepository) -> None:
        self.event_repository = event_repository
        self.ticket_repository = ticket_repository

    def execute(self, input_data: CancelTicketInput) -> CancelTicketOutput:
        # Step 1: Retrieve the ticket
        ticket = self.ticket_repository.find_by_id(input_data.ticket_id)
        if not ticket:
            return CancelTicketOutput(ticket=None, success=False, message=f"Ticket '{input_data.ticket_id}' not found")

        # Step 2: Validate purchaser ownership
        if ticket.purchaser_email.strip().lower() != input_data.purchaser_email.strip().lower():
            return CancelTicketOutput(ticket=None, success=False, message="Unauthorized: Email does not match purchaser email")

        # Step 3: Check status and mark as cancelled on the Ticket entity
        try:
            ticket.cancel()
        except ValueError as exc:
            return CancelTicketOutput(ticket=ticket, success=False, message=str(exc))

        # Step 4: Retrieve the corresponding event and release stock
        event = self.event_repository.find_by_id(ticket.event_id)
        if not event:
            return CancelTicketOutput(ticket=None, success=False, message="Event associated with ticket was not found")

        try:
            event.release_ticket(ticket.category_name)
        except ValueError as exc:
            return CancelTicketOutput(ticket=None, success=False, message=f"Failed to release ticket stock: {str(exc)}")

        # Step 5: Persist both changes
        self.event_repository.update(event)
        updated_ticket = self.ticket_repository.update(ticket)

        return CancelTicketOutput(
            ticket=updated_ticket,
            success=True,
            message="Ticket successfully cancelled and refunded. Seat freed up."
        )
