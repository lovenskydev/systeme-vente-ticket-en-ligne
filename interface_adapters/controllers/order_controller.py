from use_cases.create_order import CreateOrderUseCase


class OrderController:
    def __init__(self, use_case: CreateOrderUseCase):
        self.use_case = use_case

    def create_order(self, request_data: dict) -> dict:
        try:
            order = self.use_case.execute(
                user_id=request_data["user_id"],
                category_id=request_data["category_id"],
                quantity=request_data["quantity"],
            )
            return {
                "success": True,
                "order_id": order.id,
                "amount": order.total_amount,
            }
        except ValueError as e:
            return {"success": False, "error": str(e)}
