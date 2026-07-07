from domain.entities.ticket import Ticket


class TicketRepository:
    def __init__(self, connection):
        self.connection = connection

    def save(self, ticket: Ticket) -> Ticket:
        cursor = self.connection.cursor()
        sql = """INSERT INTO ticket (category_id, order_id, unique_code, used)
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (
            ticket.category_id,
            ticket.order_id,
            ticket.unique_code,
            ticket.used,
        ))
        self.connection.commit()
        ticket.id = cursor.lastrowid
        return ticket

    def find_by_id(self, ticket_id: int) -> Ticket:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ticket WHERE id = %s", (ticket_id,))
        row = cursor.fetchone()
        if row:
            return Ticket(**row)
        return None

    def update(self, ticket: Ticket) -> None:
        cursor = self.connection.cursor()
        sql = "UPDATE ticket SET used = %s WHERE id = %s"
        cursor.execute(sql, (ticket.used, ticket.id))
        self.connection.commit()
