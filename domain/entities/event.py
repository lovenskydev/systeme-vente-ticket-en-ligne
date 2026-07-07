from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    id: int
    title: str
    description: str
    event_date: datetime
    location: str
    organizer_id: int

    def is_past(self) -> bool:
        return self.event_date < datetime.now()
