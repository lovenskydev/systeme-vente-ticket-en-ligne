import uuid
from domain.entities.ticket import Ticket


class BuyTicketUseCase:
    def __init__(self, ticket_repo):
        self.ticket_repo = ticket_repo

    def execute(self, category_id: int, order_id: int) -> Ticket:
        ticket = Ticket(
            id=None,
            category_id=category_id,
            order_id=order_id,
            unique_code=str(uuid.uuid4()),
        )
        return self.ticket_repo.save(ticket)
