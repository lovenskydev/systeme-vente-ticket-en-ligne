from dataclasses import dataclass


@dataclass
class TicketCategory:
    id: int
    event_id: int
    name: str          # ex : VIP, Standard
    price: float
    available_quantity: int

    def is_available(self) -> bool:
        return self.available_quantity > 0
