from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    id: int
    user_id: int
    order_date: datetime
    total_amount: float
    status: str = "pending"  # en attente, payée, annulée

    def confirm_payment(self):
        self.status = "paid"
