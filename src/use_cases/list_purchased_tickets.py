from dataclasses import dataclass
from typing import List
from src.entities.ticket import Ticket
from src.use_cases.interfaces.ticket_repository import TicketRepository

@dataclass
class ListPurchasedTicketsInput:
    purchaser_email: str

@dataclass
class ListPurchasedTicketsOutput:
    tickets: List[Ticket]
    success: bool
    message: str

class ListPurchasedTicketsUseCase:
    def __init__(self, ticket_repository: TicketRepository) -> None:
        self.ticket_repository = ticket_repository

    def execute(self, input_data: ListPurchasedTicketsInput) -> ListPurchasedTicketsOutput:
        email = input_data.purchaser_email.strip()
        if not email or "@" not in email:
            return ListPurchasedTicketsOutput(tickets=[], success=False, message="Invalid purchaser email format")
            
        tickets = self.ticket_repository.find_by_purchaser(email)
        return ListPurchasedTicketsOutput(
            tickets=tickets,
            success=True,
            message=f"Found {len(tickets)} tickets for '{email}'"
        )
