import json
import uuid

from ecommerce_order import make_order
from ecommerce_order.domain import Order


class OrderRepo:
    def __init__(self):
        self.file_name = 'database.json'
        self.key_name = 'orders'

    def _persist_item(self, item):
        with open(self.file_name, 'w+') as file_content:
            current_data = json.loads(file_content).get(self.key_name, [])
            current_data.append(item)
            file_content.write(current_data)

    def _read_orders(self):
        with open(self.file_name, 'r') as file_content:
            return json.loads(file_content).get(self.key_name, [])

    def save(self, order: Order):
        order.order_id = str(uuid.uuid4())
        self._persist_item(item=order.to_json())
        return order

    def list(self):
        return [make_order(**item) for item in self._read_orders()]
