import unittest
from domain.entities.ticket import Ticket


class TestTicket(unittest.TestCase):

    def test_validate_unused_ticket(self):
        ticket = Ticket(id=1, category_id=1, order_id=1, unique_code="ABC123")
        ticket.validate()
        self.assertTrue(ticket.used)

    def test_validate_already_used_ticket_raises_error(self):
        ticket = Ticket(id=1, category_id=1, order_id=1, unique_code="ABC123", used=True)
        with self.assertRaises(ValueError):
            ticket.validate()


if __name__ == "__main__":
    unittest.main()
