from product_api.domain import Product
from product_api import make_repo


class ProductService:
    def __init__(self):
        self.repo = make_repo()

    def list(self):
        return self.repo.list()

    def add(self, product: Product):
        self.repo.save(product)
        return product.to_json()

    def get(self, product_id):
        product = self.repo.get(product_id)
        return product.to_json()
