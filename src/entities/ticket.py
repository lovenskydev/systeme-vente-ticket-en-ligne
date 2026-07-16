from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import uuid

def _now() -> datetime:
    return datetime.now(timezone.utc)

class TicketStatus(Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    USED = "used"

@dataclass
class Ticket:
    event_id: str
    event_name: str
    category_name: str
    price: float
    purchaser_email: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TicketStatus = field(default=TicketStatus.ACTIVE)
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    def __post_init__(self) -> None:
        if not self.event_id or not self.event_id.strip():
            raise ValueError("Event ID cannot be empty")
        if not self.event_name or not self.event_name.strip():
            raise ValueError("Event name cannot be empty")
        if not self.category_name or not self.category_name.strip():
            raise ValueError("Category name cannot be empty")
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        
        self.purchaser_email = self.purchaser_email.strip()
        if not self.purchaser_email or "@" not in self.purchaser_email:
            raise ValueError("Invalid purchaser email format")
            
        self.event_id = self.event_id.strip()
        self.event_name = self.event_name.strip()
        self.category_name = self.category_name.strip()

    def cancel(self) -> None:
        """
        Business Rule: Mark a ticket as cancelled.
        Only ACTIVE tickets can be cancelled.
        """
        if self.status == TicketStatus.CANCELLED:
            raise ValueError("Ticket is already cancelled")
        if self.status == TicketStatus.USED:
            raise ValueError("Cannot cancel a ticket that has already been used")
        self.status = TicketStatus.CANCELLED
        self.updated_at = _now()

    def validate(self) -> None:
        """
        Business Rule: Mark a ticket as used at the entrance.
        Only ACTIVE tickets can be validated.
        """
        if self.status == TicketStatus.USED:
            raise ValueError("Ticket has already been used")
        if self.status == TicketStatus.CANCELLED:
            raise ValueError("Cannot validate a cancelled ticket")
        self.status = TicketStatus.USED
        self.updated_at = _now()
