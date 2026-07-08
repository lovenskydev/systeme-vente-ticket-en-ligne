import unittest
from domain.entities.ticket_category import TicketCategory


class TestTicketCategory(unittest.TestCase):

    def test_is_available_when_quantity_positive(self):
        category = TicketCategory(id=1, event_id=1, name="VIP", price=50.0, available_quantity=10)
        self.assertTrue(category.is_available())

    def test_is_not_available_when_quantity_zero(self):
        category = TicketCategory(id=1, event_id=1, name="VIP", price=50.0, available_quantity=0)
        self.assertFalse(category.is_available())


if __name__ == "__main__":
    unittest.main()
