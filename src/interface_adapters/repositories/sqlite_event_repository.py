import sqlite3
import json
from datetime import datetime, timezone
from typing import List, Optional

from src.entities.event import Event, EventCategory
from src.use_cases.interfaces.event_repository import EventRepository

_DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

class SQLiteEventRepository(EventRepository):
    """
    Adapter: persists events to a SQLite database.
    """

    def __init__(self, db_path: str = "ticketing.db") -> None:
        self.db_path = db_path
        self._init_schema()

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id              TEXT PRIMARY KEY,
                    title           TEXT NOT NULL,
                    description     TEXT NOT NULL DEFAULT '',
                    categories_json TEXT NOT NULL,
                    created_at      TEXT NOT NULL,
                    updated_at      TEXT NOT NULL
                )
            """)

    def save(self, event: Event) -> Event:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO events (id, title, description, categories_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                self._to_row(event),
            )
        return event

    def find_by_id(self, event_id: str) -> Optional[Event]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,))
            row = cursor.fetchone()
            if row:
                return self._from_row(row)
            
            # If not found, try prefix matching
            cursor = conn.execute("SELECT * FROM events WHERE id LIKE ?", (f"{event_id}%",))
            rows = cursor.fetchall()
            if len(rows) == 1:
                return self._from_row(rows[0])
        return None

    def find_all(self) -> List[Event]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM events")
            rows = cursor.fetchall()
        return [self._from_row(r) for r in rows]

    def update(self, event: Event) -> Event:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE events
                SET title = ?, description = ?, categories_json = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    event.title,
                    event.description,
                    json.dumps({
                        name: {
                            "name": cat.name,
                            "price": cat.price,
                            "total_capacity": cat.total_capacity,
                            "available_seats": cat.available_seats
                        }
                        for name, cat in event.categories.items()
                    }),
                    event.updated_at.strftime(_DT_FORMAT),
                    event.id,
                ),
            )
        return event

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _to_row(self, event: Event) -> tuple:
        categories_dict = {
            name: {
                "name": cat.name,
                "price": cat.price,
                "total_capacity": cat.total_capacity,
                "available_seats": cat.available_seats
            }
            for name, cat in event.categories.items()
        }
        return (
            event.id,
            event.title,
            event.description,
            json.dumps(categories_dict),
            event.created_at.strftime(_DT_FORMAT),
            event.updated_at.strftime(_DT_FORMAT),
        )

    def _from_row(self, row: sqlite3.Row) -> Event:
        categories_dict = json.loads(row["categories_json"])
        categories = {
            name: EventCategory(
                name=cat["name"],
                price=cat["price"],
                total_capacity=cat["total_capacity"],
                available_seats=cat["available_seats"]
            )
            for name, cat in categories_dict.items()
        }
        return Event(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            categories=categories,
            created_at=datetime.strptime(row["created_at"], _DT_FORMAT).replace(tzinfo=timezone.utc),
            updated_at=datetime.strptime(row["updated_at"], _DT_FORMAT).replace(tzinfo=timezone.utc),
        )
