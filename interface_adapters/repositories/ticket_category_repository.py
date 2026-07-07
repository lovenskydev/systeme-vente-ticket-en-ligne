from use_cases.interfaces.repositories import TicketCategoryRepositoryInterface
from domain.entities.ticket_category import TicketCategory


class TicketCategoryRepository(TicketCategoryRepositoryInterface):
    def __init__(self, connection):
        self.connection = connection

    def find_by_id(self, category_id: int) -> TicketCategory:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ticket_category WHERE id = %s", (category_id,))
        row = cursor.fetchone()
        if row:
            return TicketCategory(**row)
        return None

    def update(self, category: TicketCategory) -> None:
        cursor = self.connection.cursor()
        sql = "UPDATE ticket_category SET available_quantity = %s WHERE id = %s"
        cursor.execute(sql, (category.available_quantity, category.id))
        self.connection.commit()
