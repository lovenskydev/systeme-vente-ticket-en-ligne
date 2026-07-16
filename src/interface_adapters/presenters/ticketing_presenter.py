from typing import Any, Dict, List
from src.entities.event import Event, EventCategory
from src.entities.ticket import Ticket

class TicketingPresenter:
    """
    Presenter: translates Ticketing entities into serializable dicts
    or display-friendly strings.
    """

    @staticmethod
    def event_to_dict(event: Event) -> Dict[str, Any]:
        return {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "categories": {
                name: {
                    "name": cat.name,
                    "price": cat.price,
                    "total_capacity": cat.total_capacity,
                    "available_seats": cat.available_seats
                }
                for name, cat in event.categories.items()
            },
            "created_at": event.created_at.isoformat(),
            "updated_at": event.updated_at.isoformat()
        }

    @staticmethod
    def event_list_to_dicts(events: List[Event]) -> List[Dict[str, Any]]:
        return [TicketingPresenter.event_to_dict(e) for e in events]

    @staticmethod
    def ticket_to_dict(ticket: Ticket) -> Dict[str, Any]:
        return {
            "id": ticket.id,
            "event_id": ticket.event_id,
            "event_name": ticket.event_name,
            "category_name": ticket.category_name,
            "price": ticket.price,
            "purchaser_email": ticket.purchaser_email,
            "status": ticket.status.value,
            "created_at": ticket.created_at.isoformat(),
            "updated_at": ticket.updated_at.isoformat()
        }

    @staticmethod
    def ticket_list_to_dicts(tickets: List[Ticket]) -> List[Dict[str, Any]]:
        return [TicketingPresenter.ticket_to_dict(t) for t in tickets]

    @staticmethod
    def format_event_row(event: Event) -> str:
        """
        Format event summary row.
        """
        return f"  ID: {event.id[:8]} | {event.title:<30} - {event.description}"

    @staticmethod
    def format_category_row(cat: EventCategory) -> str:
        """
        Format category row showing stock and pricing.
        """
        return f"    - {cat.name:<15} Price: ${cat.price:<6.2f} | Available Stock: {cat.available_seats}/{cat.total_capacity}"

    @staticmethod
    def format_ticket_row(ticket: Ticket) -> str:
        """
        Format a single row for list view.
        """
        status_icon = {
            "active": "[Active]",
            "cancelled": "[Cancelled]",
            "used": "[Used]"
        }.get(ticket.status.value, "[Unknown]")
        
        return (
            f"  {status_icon:<12} Code: {ticket.id:<36} | "
            f"Event: {ticket.event_name:<20} | Category: {ticket.category_name:<10} | Price: ${ticket.price:.2f}"
        )
