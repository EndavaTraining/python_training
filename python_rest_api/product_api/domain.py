import uuid


class Product:
    def __init__(self, title, price, stock, product_id=None):
        self.product_id = str(uuid.uuid4()) if product_id is None else product_id
        self.title = title
        self.price = price
        self.stock = stock

    def to_json(self):
        return {
            'product_id': self.product_id,
            'title': self.title,
            'price': self.price,
            'stock': self.stock,
        }
