import sqlite3
from datetime import datetime, timezone
from typing import List, Optional

from src.entities.ticket import Ticket, TicketStatus
from src.use_cases.interfaces.ticket_repository import TicketRepository

_DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

class SQLiteTicketRepository(TicketRepository):
    """
    Adapter: persists tickets to a SQLite database.
    """

    def __init__(self, db_path: str = "ticketing.db") -> None:
        self.db_path = db_path
        self._init_schema()

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id              TEXT PRIMARY KEY,
                    event_id        TEXT NOT NULL,
                    event_name      TEXT NOT NULL,
                    category_name   TEXT NOT NULL,
                    price           REAL NOT NULL,
                    purchaser_email TEXT NOT NULL,
                    status          TEXT NOT NULL,
                    created_at      TEXT NOT NULL,
                    updated_at      TEXT NOT NULL
                )
            """)

    def save(self, ticket: Ticket) -> Ticket:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO tickets (id, event_id, event_name, category_name, price, purchaser_email, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                self._to_row(ticket),
            )
        return ticket

    def find_by_id(self, ticket_id: str) -> Optional[Ticket]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
            row = cursor.fetchone()
            if row:
                return self._from_row(row)
            
            # If not found, try prefix matching
            cursor = conn.execute("SELECT * FROM tickets WHERE id LIKE ?", (f"{ticket_id}%",))
            rows = cursor.fetchall()
            if len(rows) == 1:
                return self._from_row(rows[0])
        return None

    def find_by_purchaser(self, purchaser_email: str) -> List[Ticket]:
        normalized_email = purchaser_email.strip().lower()
        with self._connect() as conn:
            # Note: email search can be case-insensitive, let's normalize or compare using SQL lower() or post-process.
            # SQL lower() is reliable.
            cursor = conn.execute("SELECT * FROM tickets WHERE LOWER(purchaser_email) = ?", (normalized_email,))
            rows = cursor.fetchall()
        return [self._from_row(r) for r in rows]

    def update(self, ticket: Ticket) -> Ticket:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE tickets
                SET status = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    ticket.status.value,
                    ticket.updated_at.strftime(_DT_FORMAT),
                    ticket.id,
                ),
            )
        return ticket

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _to_row(self, ticket: Ticket) -> tuple:
        return (
            ticket.id,
            ticket.event_id,
            ticket.event_name,
            ticket.category_name,
            ticket.price,
            ticket.purchaser_email,
            ticket.status.value,
            ticket.created_at.strftime(_DT_FORMAT),
            ticket.updated_at.strftime(_DT_FORMAT),
        )

    def _from_row(self, row: sqlite3.Row) -> Ticket:
        return Ticket(
            id=row["id"],
            event_id=row["event_id"],
            event_name=row["event_name"],
            category_name=row["category_name"],
            price=row["price"],
            purchaser_email=row["purchaser_email"],
            status=TicketStatus(row["status"]),
            created_at=datetime.strptime(row["created_at"], _DT_FORMAT).replace(tzinfo=timezone.utc),
            updated_at=datetime.strptime(row["updated_at"], _DT_FORMAT).replace(tzinfo=timezone.utc),
        )
