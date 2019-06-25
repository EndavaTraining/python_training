import uuid


class Order:
    def __init__(self, items, user_id, order_id=None, status="CREATED"):
        self.order_id = str(uuid.uuid4()) if order_id is None else order_id
        self.status = status
        self.user_id = user_id
        self.items = items

    def to_json(self):
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'items': self.items,
            'status': self.status,
        }
