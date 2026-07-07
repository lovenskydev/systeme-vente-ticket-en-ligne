from dataclasses import dataclass


@dataclass
class Ticket:
    id: int
    category_id: int
    order_id: int
    unique_code: str
    used: bool = False

    def validate(self):
        if self.used:
            raise ValueError("This ticket has already been used")
        self.used = True
