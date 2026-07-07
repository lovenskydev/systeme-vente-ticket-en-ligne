from datetime import datetime
from domain.entities.order import Order
from use_cases.interfaces.repositories import (
    OrderRepositoryInterface,
    TicketCategoryRepositoryInterface,
)


class CreateOrderUseCase:
    def __init__(
        self,
        order_repo: OrderRepositoryInterface,
        category_repo: TicketCategoryRepositoryInterface,
    ):
        self.order_repo = order_repo
        self.category_repo = category_repo

    def execute(self, user_id: int, category_id: int, quantity: int) -> Order:
        category = self.category_repo.find_by_id(category_id)

        if category.available_quantity < quantity:
            raise ValueError("Not enough tickets available")

        total_amount = category.price * quantity

        order = Order(
            id=None,
            user_id=user_id,
            order_date=datetime.now(),
            total_amount=total_amount,
        )

        saved_order = self.order_repo.save(order)

        category.available_quantity -= quantity
        self.category_repo.update(category)

        return saved_order
