import json

from order_api import make_order
from order_api.domain import Order
from order_api.repo import RepoInterface


class OrderFileRepo(RepoInterface):
    def __init__(self):
        self.file_name = 'database.json'
        self.key_name = 'orders'

    def _persist_item(self, item):
        with open(self.file_name) as file_content:
            current_data = json.load(file_content)

        current_data_orders = current_data.get(self.key_name, [])
        current_data_orders.append(item)
        current_data[self.key_name] = current_data_orders

        with open(self.file_name, 'w') as file:
            json.dump(current_data, file)

    def _read_orders(self):
        with open(self.file_name) as file_content:
            file_contents = json.load(file_content)
            return file_contents.get(self.key_name, [])

    def save(self, order: Order):
        self._persist_item(item=order.to_json())
        return order

    def list(self):
        return [make_order(**item) for item in self._read_orders()]
