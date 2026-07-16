import copy
from typing import Dict, List, Optional
from src.entities.event import Event
from src.use_cases.interfaces.event_repository import EventRepository

class InMemoryEventRepository(EventRepository):
    """
    Adapter: stores events in a dict in process memory.
    """

    def __init__(self) -> None:
        self._store: Dict[str, Event] = {}

    def save(self, event: Event) -> Event:
        if event.id in self._store:
            raise ValueError(f"Event with id '{event.id}' already exists")
        self._store[event.id] = copy.deepcopy(event)
        return copy.deepcopy(self._store[event.id])

    def find_by_id(self, event_id: str) -> Optional[Event]:
        event = self._store.get(event_id)
        if event:
            return copy.deepcopy(event)
        # Try prefix matching
        matches = [e for e in self._store.values() if e.id.startswith(event_id)]
        if len(matches) == 1:
            return copy.deepcopy(matches[0])
        return None

    def find_all(self) -> List[Event]:
        return [copy.deepcopy(e) for e in self._store.values()]

    def update(self, event: Event) -> Event:
        if event.id not in self._store:
            raise ValueError(f"Event with id '{event.id}' not found — cannot update")
        self._store[event.id] = copy.deepcopy(event)
        return copy.deepcopy(self._store[event.id])
