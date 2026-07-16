import os
from src.interface_adapters.repositories.sqlite_event_repository import SQLiteEventRepository
from src.interface_adapters.repositories.sqlite_ticket_repository import SQLiteTicketRepository
from src.interface_adapters.controllers.ticketing_controller import TicketingController
from src.frameworks.cli.cli_app import run_cli

from src.entities.event import Event, EventCategory

def _seed_data(event_repo: SQLiteEventRepository) -> None:
    """
    Seed initial sample events with ticket categories and stock.
    """
    events = [
        Event(
            id="event-1",
            title="Tech Innovators Summit 2026",
            description="The premier technology event of the year, showcasing advances in Artificial Intelligence.",
            categories={
                "VIP": EventCategory(name="VIP", price=250.0, total_capacity=5, available_seats=5),
                "Regular": EventCategory(name="Regular", price=75.0, total_capacity=50, available_seats=50),
            }
        ),
        Event(
            id="event-2",
            title="Rock Legend Reunion Concert",
            description="Experience the legendary rock band reunion live in concert under the stars!",
            categories={
                "FrontRow": EventCategory(name="FrontRow", price=150.0, total_capacity=10, available_seats=10),
                "General": EventCategory(name="General", price=45.0, total_capacity=300, available_seats=300),
            }
        ),
        Event(
            id="event-3",
            title="World Championship Final",
            description="The epic final match to determine the soccer world champions.",
            categories={
                "Premium": EventCategory(name="Premium", price=300.0, total_capacity=3, available_seats=3),
                "StandA": EventCategory(name="StandA", price=120.0, total_capacity=100, available_seats=100),
                "StandB": EventCategory(name="StandB", price=60.0, total_capacity=200, available_seats=200),
            }
        )
    ]
    
    for event in events:
        event_repo.save(event)

def main() -> None:
    # Define database path in workspace
    db_path = "ticketing.db"
    
    # Instantiate SQLite repositories
    event_repo = SQLiteEventRepository(db_path)
    ticket_repo = SQLiteTicketRepository(db_path)
    
    # Seed data if no events exist
    try:
        if len(event_repo.find_all()) == 0:
            _seed_data(event_repo)
    except Exception as exc:
        print(f"Error checking or seeding database: {exc}")
        
    # Wire controllers
    controller = TicketingController(event_repo, ticket_repo)
    
    # Run the interactive CLI delivery mechanism
    run_cli(controller)

if __name__ == "__main__":
    main()
