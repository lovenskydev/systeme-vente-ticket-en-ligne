from abc import ABC, abstractmethod
from typing import List, Optional
from src.entities.event import Event

class EventRepository(ABC):
    """
    Abstract Port for Event persistence.
    """

    @abstractmethod
    def save(self, event: Event) -> Event:
        """Persist a new event. Returns the saved event."""
        ...

    @abstractmethod
    def find_by_id(self, event_id: str) -> Optional[Event]:
        """Retrieve an event by ID. Returns None if not found."""
        ...

    @abstractmethod
    def find_all(self) -> List[Event]:
        """Retrieve all events."""
        ...

    @abstractmethod
    def update(self, event: Event) -> Event:
        """Update an existing event (e.g. updating seat availability)."""
        ...
