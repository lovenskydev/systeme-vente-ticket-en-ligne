from typing import Any, Dict
from src.use_cases.list_events import ListEventsInput, ListEventsUseCase
from src.use_cases.buy_ticket import BuyTicketInput, BuyTicketUseCase
from src.use_cases.list_purchased_tickets import ListPurchasedTicketsInput, ListPurchasedTicketsUseCase
from src.use_cases.cancel_ticket import CancelTicketInput, CancelTicketUseCase
from src.use_cases.validate_ticket import ValidateTicketInput, ValidateTicketUseCase
from src.use_cases.get_event import GetEventInput, GetEventUseCase

from src.interface_adapters.presenters.ticketing_presenter import TicketingPresenter
from src.use_cases.interfaces.event_repository import EventRepository
from src.use_cases.interfaces.ticket_repository import TicketRepository

class TicketingController:
    """
    Traffic director orchestrating all ticketing-related use cases.
    """

    def __init__(self, event_repository: EventRepository, ticket_repository: TicketRepository) -> None:
        self.list_events_use_case = ListEventsUseCase(event_repository)
        self.buy_ticket_use_case = BuyTicketUseCase(event_repository, ticket_repository)
        self.list_purchased_tickets_use_case = ListPurchasedTicketsUseCase(ticket_repository)
        self.cancel_ticket_use_case = CancelTicketUseCase(event_repository, ticket_repository)
        self.validate_ticket_use_case = ValidateTicketUseCase(ticket_repository)
        self.get_event_use_case = GetEventUseCase(event_repository)

    def list_events(self) -> Dict[str, Any]:
        output = self.list_events_use_case.execute(ListEventsInput())
        return {
            "success": True,
            "events": [TicketingPresenter.event_to_dict(e) for e in output.events],
            "total": output.total
        }

    def buy_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        event_id = data.get("event_id", "").strip()
        category_name = data.get("category_name", "").strip()
        purchaser_email = data.get("purchaser_email", "").strip()

        if not event_id:
            return {"success": False, "error": "Event ID is required"}
        if not category_name:
            return {"success": False, "error": "Category name is required"}
        if not purchaser_email:
            return {"success": False, "error": "Purchaser email is required"}

        output = self.buy_ticket_use_case.execute(
            BuyTicketInput(
                event_id=event_id,
                category_name=category_name,
                purchaser_email=purchaser_email
            )
        )
        if not output.success:
            return {"success": False, "error": output.message}

        return {
            "success": True,
            "message": output.message,
            "ticket": TicketingPresenter.ticket_to_dict(output.ticket)
        }

    def list_purchased_tickets(self, purchaser_email: str) -> Dict[str, Any]:
        email = purchaser_email.strip()
        if not email:
            return {"success": False, "error": "Purchaser email is required"}

        output = self.list_purchased_tickets_use_case.execute(
            ListPurchasedTicketsInput(purchaser_email=email)
        )
        if not output.success:
            return {"success": False, "error": output.message}

        return {
            "success": True,
            "message": output.message,
            "tickets": [TicketingPresenter.ticket_to_dict(t) for t in output.tickets]
        }

    def cancel_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        ticket_id = data.get("ticket_id", "").strip()
        purchaser_email = data.get("purchaser_email", "").strip()

        if not ticket_id:
            return {"success": False, "error": "Ticket code is required"}
        if not purchaser_email:
            return {"success": False, "error": "Purchaser email is required"}

        output = self.cancel_ticket_use_case.execute(
            CancelTicketInput(ticket_id=ticket_id, purchaser_email=purchaser_email)
        )
        if not output.success:
            return {"success": False, "error": output.message}

        return {
            "success": True,
            "message": output.message,
            "ticket": TicketingPresenter.ticket_to_dict(output.ticket)
        }

    def validate_ticket(self, ticket_id: str) -> Dict[str, Any]:
        tid = ticket_id.strip()
        if not tid:
            return {"success": False, "error": "Ticket code is required"}

        output = self.validate_ticket_use_case.execute(
            ValidateTicketInput(ticket_id=tid)
        )
        if not output.success:
            return {"success": False, "error": output.message}

        return {
            "success": True,
            "message": output.message,
            "ticket": TicketingPresenter.ticket_to_dict(output.ticket)
        }

    def get_event(self, event_id: str) -> Dict[str, Any]:
        output = self.get_event_use_case.execute(GetEventInput(event_id=event_id))
        if not output.success:
            return {"success": False, "error": output.message}
        return {"success": True, "event": TicketingPresenter.event_to_dict(output.event)}
