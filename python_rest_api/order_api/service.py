from order_api.domain import Order
from order_api import make_repo


class OrderService:
    def __init__(self):
        self.repo = make_repo()

    def list(self):
        return self.repo.list()

    def add(self, order: Order):
        self.repo.save(order)
        return order.to_json()
