import sys
from src.interface_adapters.controllers.ticketing_controller import TicketingController
from src.interface_adapters.presenters.ticketing_presenter import TicketingPresenter

# ANSI color helpers
class _C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    GREEN  = "\033[32m"
    YELLOW = "\033[33m"
    CYAN   = "\033[36m"
    RED    = "\033[31m"
    MAGENTA = "\033[35m"

def _banner(text: str) -> None:
    print(f"\n{_C.BOLD}{_C.MAGENTA}{'=' * 50}{_C.RESET}")
    print(f"{_C.BOLD}{_C.CYAN}  {text}{_C.RESET}")
    print(f"{_C.BOLD}{_C.MAGENTA}{'=' * 50}{_C.RESET}\n")

def _ok(msg: str) -> None:
    print(f"{_C.GREEN}  ✓  {msg}{_C.RESET}")

def _err(msg: str) -> None:
    print(f"{_C.RED}  ✗  {msg}{_C.RESET}")

def run_cli(controller: TicketingController) -> None:
    """
    Interactive CLI run loop.
    """
    _banner("TICKETING SYSTEM 🎟️")
    
    while True:
        print(f"\n{_C.BOLD}Please choose an option:{_C.RESET}")
        print("1) View events & pricing (Includes details, categories, & prices)")
        print("2) Buy a ticket (Handles order creation & stock management)")
        print("3) View my purchased tickets (New - essential!)")
        print("4) Cancel a ticket (Refund / Free up seat)")
        print("5) [ADMIN] Validate a ticket at entrance (Mark as 'used')")
        print("6) Exit")
        
        try:
            choice = input(f"\n{_C.BOLD}Option (1-6) > {_C.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Thank you!")
            break

        if choice == "1":
            print(f"\n{_C.BOLD}--- Available Events & Pricing ---{_C.RESET}")
            result = controller.list_events()
            if not result["success"]:
                _err(result.get("error", "Failed to retrieve events"))
                continue
            
            if result["total"] == 0:
                print("  No events available currently.")
            else:
                for event_dict in result["events"]:
                    print(f"\n{_C.BOLD}{_C.CYAN}Event: {event_dict['title']} (ID: {event_dict['id']}){_C.RESET}")
                    print(f"  Description : {event_dict['description']}")
                    print(f"  Categories  :")
                    for cat_name, cat in event_dict["categories"].items():
                        print(f"    - {cat_name:<12} | Price: ${cat['price']:<6.2f} | Stock: {cat['available_seats']}/{cat['total_capacity']}")
                print(f"\n  Total Events: {result['total']}")

        elif choice == "2":
            print(f"\n{_C.BOLD}--- Buy a Ticket ---{_C.RESET}")
            event_id = input("  Event ID (or prefix) : ").strip()
            
            # Fetch the event to list categories dynamically
            event_result = controller.get_event(event_id)
            if not event_result["success"]:
                _err(event_result["error"])
                continue
                
            event_data = event_result["event"]
            categories = list(event_data["categories"].keys())
            
            if not categories:
                _err("No categories defined for this event.")
                continue

            print("\n  Select Category:")
            for idx, cat_name in enumerate(categories, 1):
                cat = event_data["categories"][cat_name]
                print(f"    {idx}) {cat_name:<12} | Price: ${cat['price']:.2f} | Stock: {cat['available_seats']}/{cat['total_capacity']}")
            
            try:
                cat_idx_str = input(f"\n  Choose category (1-{len(categories)}) > ").strip()
                cat_idx = int(cat_idx_str) - 1
                if cat_idx < 0 or cat_idx >= len(categories):
                    raise ValueError("Selection out of range")
                category_name = categories[cat_idx]
            except ValueError:
                _err("Invalid category selection")
                continue

            purchaser_email = input("  Your Email Address   : ").strip()

            result = controller.buy_ticket({
                "event_id": event_data["id"], # Use the full resolved ID
                "category_name": category_name,
                "purchaser_email": purchaser_email
            })
            if result["success"]:
                _ok(result["message"])
                t = result["ticket"]
                print(f"    Code     : {t['id']}")
                print(f"    Event    : {t['event_name']}")
                print(f"    Category : {t['category_name']}")
                print(f"    Price    : ${t['price']:.2f}")
            else:
                _err(result["error"])

        elif choice == "3":
            print(f"\n{_C.BOLD}--- View My Purchased Tickets ---{_C.RESET}")
            purchaser_email = input("  Enter Your Email Address: ").strip()
            result = controller.list_purchased_tickets(purchaser_email)
            if result["success"]:
                tickets = result["tickets"]
                if not tickets:
                    print(f"  No tickets found for '{purchaser_email}'")
                else:
                    print(f"\n  Tickets purchased by {purchaser_email}:")
                    print(f"  {'-'*80}")
                    for t in tickets:
                        status_icon = {
                            "active": f"{_C.GREEN}[Active]{_C.RESET}",
                            "cancelled": f"{_C.RED}[Cancelled]{_C.RESET}",
                            "used": f"{_C.YELLOW}[Used]{_C.RESET}"
                        }.get(t["status"], "[Unknown]")
                        
                        print(
                            f"  {status_icon:<20} Code: {t['id'][:8]}... | "
                            f"Event: {t['event_name']:<18} | Cat: {t['category_name']:<10} | Price: ${t['price']:.2f}"
                        )
                    print(f"  {'-'*80}")
                    print(f"  Total: {len(tickets)}")
            else:
                _err(result["error"])

        elif choice == "4":
            print(f"\n{_C.BOLD}--- Cancel a Ticket (Refund) ---{_C.RESET}")
            ticket_id = input("  Ticket Code (or prefix) : ").strip()
            purchaser_email = input("  Purchaser Email         : ").strip()

            result = controller.cancel_ticket({
                "ticket_id": ticket_id,
                "purchaser_email": purchaser_email
            })
            if result["success"]:
                _ok(result["message"])
            else:
                _err(result["error"])

        elif choice == "5":
            print(f"\n{_C.BOLD}--- [ADMIN] Validate a Ticket at Entrance ---{_C.RESET}")
            ticket_id = input("  Ticket Code (or prefix): ").strip()

            result = controller.validate_ticket(ticket_id)
            if result["success"]:
                _ok(result["message"])
                t = result["ticket"]
                print(f"    Event    : {t['event_name']}")
                print(f"    Category : {t['category_name']}")
                print(f"    Holder   : {t['purchaser_email']}")
            else:
                _err(result["error"])

        elif choice == "6":
            print("\nExiting Ticket System. Goodbye! 👋")
            break

        else:
            print(f"  {_C.RED}Invalid choice: '{choice}'. Please pick a number from 1 to 6.{_C.RESET}")
