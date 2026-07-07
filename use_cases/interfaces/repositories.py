from abc import ABC, abstractmethod
from domain.entities.order import Order
from domain.entities.ticket_category import TicketCategory


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def find_by_id(self, order_id: int) -> Order:
        pass


class TicketCategoryRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, category_id: int) -> TicketCategory:
        pass

    @abstractmethod
    def update(self, category: TicketCategory) -> None:
        pass
