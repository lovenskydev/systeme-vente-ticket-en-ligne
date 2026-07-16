from dataclasses import dataclass
from typing import Optional
from src.entities.event import Event
from src.use_cases.interfaces.event_repository import EventRepository

@dataclass
class GetEventInput:
    event_id: str

@dataclass
class GetEventOutput:
    event: Optional[Event]
    success: bool
    message: str = ""

class GetEventUseCase:
    """
    Use Case: Retrieve a single Event by its ID or prefix.
    """

    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    def execute(self, input_data: GetEventInput) -> GetEventOutput:
        event = self.repository.find_by_id(input_data.event_id)
        if not event:
            return GetEventOutput(event=None, success=False, message=f"Event '{input_data.event_id}' not found")
        return GetEventOutput(event=event, success=True)
