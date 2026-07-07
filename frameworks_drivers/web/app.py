from flask import Flask, request, jsonify

from frameworks_drivers.database.mysql_connection import create_connection
from interface_adapters.repositories.order_repository import OrderRepository
from interface_adapters.repositories.ticket_category_repository import TicketCategoryRepository
from interface_adapters.controllers.order_controller import OrderController
from use_cases.create_order import CreateOrderUseCase

app = Flask(__name__)
connection = create_connection()

order_repo = OrderRepository(connection)
category_repo = TicketCategoryRepository(connection)
use_case = CreateOrderUseCase(order_repo, category_repo)
controller = OrderController(use_case)


@app.route("/orders", methods=["POST"])
def create_order():
    result = controller.create_order(request.json)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
