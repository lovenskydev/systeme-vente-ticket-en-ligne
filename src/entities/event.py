from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid

def _now() -> datetime:
    return datetime.now(timezone.utc)

@dataclass
class EventCategory:
    name: str
    price: float
    total_capacity: int
    available_seats: int

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Category name cannot be empty")
        self.name = self.name.strip()
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.total_capacity < 0:
            raise ValueError("Total capacity cannot be negative")
        if self.available_seats < 0:
            raise ValueError("Available seats cannot be negative")
        if self.available_seats > self.total_capacity:
            raise ValueError("Available seats cannot exceed total capacity")

@dataclass
class Event:
    title: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    categories: dict[str, EventCategory] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("Event title cannot be empty")
        self.title = self.title.strip()
        if not self.categories:
            raise ValueError("Event must have at least one ticket category")

    def book_ticket(self, category_name: str) -> None:
        """
        Business Rule: Reserve a seat in a specific category.
        Decreases available_seats by 1.
        """
        if category_name not in self.categories:
            raise ValueError(f"Category '{category_name}' does not exist for this event")
        
        category = self.categories[category_name]
        if category.available_seats <= 0:
            raise ValueError(f"No tickets available for category '{category_name}'")
        
        category.available_seats -= 1
        self.updated_at = _now()

    def release_ticket(self, category_name: str) -> None:
        """
        Business Rule: Release a reserved seat back into the category.
        Increases available_seats by 1.
        """
        if category_name not in self.categories:
            raise ValueError(f"Category '{category_name}' does not exist for this event")
        
        category = self.categories[category_name]
        if category.available_seats >= category.total_capacity:
            raise ValueError(f"Cannot release ticket: category '{category_name}' is already at full capacity")
        
        category.available_seats += 1
        self.updated_at = _now()
