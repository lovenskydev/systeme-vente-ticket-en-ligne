class ValidateTicketUseCase:
    def __init__(self, ticket_repo):
        self.ticket_repo = ticket_repo

    def execute(self, ticket_id: int) -> bool:
        ticket = self.ticket_repo.find_by_id(ticket_id)
        if ticket is None:
            raise ValueError("Ticket not found")

        ticket.validate()
        self.ticket_repo.update(ticket)
        return True
