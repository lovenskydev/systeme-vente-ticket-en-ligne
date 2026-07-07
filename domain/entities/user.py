from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    name: str
    email: str
    password_hash: str
    date_created: datetime = None

    def __post_init__(self):
        if "@" not in self.email:
            raise ValueError("Invalid email")
