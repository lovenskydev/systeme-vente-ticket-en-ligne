from abc import ABC, abstractmethod
from typing import List, Optional
from src.entities.ticket import Ticket

class TicketRepository(ABC):
    """
    Abstract Port for Ticket persistence.
    """

    @abstractmethod
    def save(self, ticket: Ticket) -> Ticket:
        """Persist a new ticket. Returns the saved ticket."""
        ...

    @abstractmethod
    def find_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """Retrieve a ticket by its ID."""
        ...

    @abstractmethod
    def find_by_purchaser(self, purchaser_email: str) -> List[Ticket]:
        """Retrieve all tickets purchased by a specific email."""
        ...

    @abstractmethod
    def update(self, ticket: Ticket) -> Ticket:
        """Update an existing ticket (e.g. status transition)."""
        ...
