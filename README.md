# Online Ticket Sales System

Final-exam mini-project — American University of the Caribbean (AUC)

## Description

A user can browse an event, choose a ticket category (VIP, Standard...),
place an order, and receive a ticket with a unique code.

## Full Project Architecture
ticket_system/
│
├── domain/                          → Entities & business rules (no dependencies)
│   ├── init.py
│   └── entities/
│       ├── user.py                  → User (validates its own email)
│       ├── event.py                 → Event (knows if it's already past)
│       ├── ticket_category.py       → TicketCategory (price, available quantity)
│       ├── ticket.py                → Ticket (unique_code, validate())
│       └── order.py                 → Order (status, confirm_payment())
│
├── use_cases/                       → Application logic + interfaces
│   ├── interfaces/
│   │   └── repositories.py          → OrderRepositoryInterface, TicketCategoryRepositoryInterface
│   ├── create_order.py              → CreateOrderUseCase
│   ├── buy_ticket.py                → BuyTicketUseCase
│   └── validate_ticket.py           → ValidateTicketUseCase
│
├── interface_adapters/              → Concrete implementations (MySQL) + controllers
│   ├── repositories/
│   │   ├── order_repository.py
│   │   ├── ticket_category_repository.py
│   │   └── ticket_repository.py
│   └── controllers/
│       └── order_controller.py
│
├── frameworks_drivers/              → Technical details (Flask + MySQL)
│   ├── database/
│   │   └── mysql_connection.py
│   └── web/
│       └── app.py
│
├── tests/                           → Unit tests (domain layer)
│   ├── test_user.py
│   ├── test_ticket.py
│   └── test_ticket_category.py
│
├── requirements.txt
└── README.md

## The 4 Layers

| Layer | Role |
|---|---|
| **Domain** | Core entities (`User`, `Event`, `TicketCategory`, `Ticket`, `Order`) and their business rules. Zero external dependencies. |
| **Use Cases** | Application logic (create an order, validate a ticket). Defines interfaces that other layers must respect. |
| **Interface Adapters** | Repositories (MySQL access) and controllers linking use cases to the outside world. |
| **Frameworks & Drivers** | Technical details: Flask server and MySQL connection. |

## Dependency Rule

Dependencies always point **inward**:
frameworks_drivers → interface_adapters → use_cases → domain

`domain` knows nothing about the other layers. `use_cases` defines
interfaces (ports) that `interface_adapters` implements. `frameworks_drivers`
wires everything together (dependency injection in `app.py`).

## Why This Architecture

- Business logic (`domain`, `use_cases`) can be tested without a database.
- The framework (Flask → Django) or database (MySQL → PostgreSQL) can be
  swapped without touching the business logic.
- Each layer has a single responsibility, making the project easier to maintain.

## Installation

```bash
pip install -r requirements.txt
```

## Run the app

```bash
python -m frameworks_drivers.web.app
```

## Run the tests

```bash
python -m unittest discover -s tests -
```

## Git branches

- `main` → domain
- `use_cases` → use_cases
- `interface_adapters` → interface_adapters
- `frameworks_drivers` → frameworks_drivers

## Author

Lovensky — Computer Science Student, AUC