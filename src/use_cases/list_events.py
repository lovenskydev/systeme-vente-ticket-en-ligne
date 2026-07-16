from dataclasses import dataclass
from typing import List
from src.entities.event import Event
from src.use_cases.interfaces.event_repository import EventRepository

@dataclass
class ListEventsInput:
    pass

@dataclass
class ListEventsOutput:
    events: List[Event]
    total: int

class ListEventsUseCase:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    def execute(self, input_data: ListEventsInput) -> ListEventsOutput:
        events = self.repository.find_all()
        return ListEventsOutput(events=events, total=len(events))
