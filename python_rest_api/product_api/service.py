from product_api.domain import Product
from product_api import make_repo


class ProductService:
    def __init__(self):
        self.repo = make_repo()

    def list(self):
        with self.repo:
            return self.repo.list()

    def add(self, product: Product):
        with self.repo:
            self.repo.save(product)
            return product.to_json()
