import unittest
from domain.entities.user import User


class TestUser(unittest.TestCase):

    def test_create_valid_user(self):
        user = User(id=1, name="Lovensky", email="lovensky@test.com", password_hash="hash123")
        self.assertEqual(user.name, "Lovensky")

    def test_invalid_email_raises_error(self):
        with self.assertRaises(ValueError):
            User(id=1, name="Lovensky", email="invalid-email", password_hash="hash123")


if __name__ == "__main__":
    unittest.main()
