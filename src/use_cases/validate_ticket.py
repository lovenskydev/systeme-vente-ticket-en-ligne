from dataclasses import dataclass
from src.entities.ticket import Ticket
from src.use_cases.interfaces.ticket_repository import TicketRepository

@dataclass
class ValidateTicketInput:
    ticket_id: str

@dataclass
class ValidateTicketOutput:
    ticket: Ticket | None
    success: bool
    message: str

class ValidateTicketUseCase:
    def __init__(self, ticket_repository: TicketRepository) -> None:
        self.ticket_repository = ticket_repository

    def execute(self, input_data: ValidateTicketInput) -> ValidateTicketOutput:
        # Step 1: Retrieve the ticket
        ticket = self.ticket_repository.find_by_id(input_data.ticket_id)
        if not ticket:
            return ValidateTicketOutput(ticket=None, success=False, message=f"Ticket '{input_data.ticket_id}' not found")

        # Step 2: Transition the state to USED (checks status rules on the entity)
        try:
            ticket.validate()
        except ValueError as exc:
            return ValidateTicketOutput(ticket=ticket, success=False, message=str(exc))

        # Step 3: Persist the updated Ticket status
        updated_ticket = self.ticket_repository.update(ticket)

        return ValidateTicketOutput(
            ticket=updated_ticket,
            success=True,
            message="Ticket successfully validated at entrance. Marked as USED."
        )
