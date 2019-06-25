from product_api.domain import Product
from product_api.repo import ProductRepo


class ProductService:
    def __init__(self):
        self.repo = ProductRepo()

    def list(self):
        return self.repo.list()

    def add(self, product: Product):
        self.repo.save(product)
        return product.to_json()
