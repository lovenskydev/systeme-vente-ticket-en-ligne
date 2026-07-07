from use_cases.interfaces.repositories import OrderRepositoryInterface
from domain.entities.order import Order


class OrderRepository(OrderRepositoryInterface):
    def __init__(self, connection):
        self.connection = connection

    def save(self, order: Order) -> Order:
        cursor = self.connection.cursor()
        sql = """INSERT INTO orders (user_id, order_date, total_amount, status)
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (
            order.user_id,
            order.order_date,
            order.total_amount,
            order.status,
        ))
        self.connection.commit()
        order.id = cursor.lastrowid
        return order

    def find_by_id(self, order_id: int) -> Order:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        row = cursor.fetchone()
        if row:
            return Order(**row)
        return None
