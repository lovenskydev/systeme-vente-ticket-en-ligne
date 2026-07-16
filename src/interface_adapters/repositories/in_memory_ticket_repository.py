import copy
from typing import Dict, List, Optional
from src.entities.ticket import Ticket
from src.use_cases.interfaces.ticket_repository import TicketRepository

class InMemoryTicketRepository(TicketRepository):
    """
    Adapter: stores tickets in a dict in process memory.
    """

    def __init__(self) -> None:
        self._store: Dict[str, Ticket] = {}

    def save(self, ticket: Ticket) -> Ticket:
        if ticket.id in self._store:
            raise ValueError(f"Ticket with id '{ticket.id}' already exists")
        self._store[ticket.id] = copy.deepcopy(ticket)
        return copy.deepcopy(self._store[ticket.id])

    def find_by_id(self, ticket_id: str) -> Optional[Ticket]:
        ticket = self._store.get(ticket_id)
        if ticket:
            return copy.deepcopy(ticket)
        # Try prefix matching
        matches = [t for t in self._store.values() if t.id.startswith(ticket_id)]
        if len(matches) == 1:
            return copy.deepcopy(matches[0])
        return None

    def find_by_purchaser(self, purchaser_email: str) -> List[Ticket]:
        normalized_email = purchaser_email.strip().lower()
        return [
            copy.deepcopy(t)
            for t in self._store.values()
            if t.purchaser_email.strip().lower() == normalized_email
        ]

    def update(self, ticket: Ticket) -> Ticket:
        if ticket.id not in self._store:
            raise ValueError(f"Ticket with id '{ticket.id}' not found — cannot update")
        self._store[ticket.id] = copy.deepcopy(ticket)
        return copy.deepcopy(self._store[ticket.id])
