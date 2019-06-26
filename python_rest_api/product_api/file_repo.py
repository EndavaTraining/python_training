import json

from product_api import make_product
from product_api.domain import Product
from product_api.repo import RepoInterface


class ProductFileRepo(RepoInterface):
    def __init__(self):
        self.file_name = 'database.json'
        self.key_name = 'products'

    def _persist_item(self, item):
        with open(self.file_name) as file_content:
            current_data = json.load(file_content)

        current_data_products = current_data.get(self.key_name, [])
        current_data_products.append(item)
        current_data[self.key_name] = current_data_products

        with open(self.file_name, 'w') as file:
            json.dump(current_data, file)

    def _read_products(self):
        with open(self.file_name) as file_content:
            file_contents = json.load(file_content)
            return file_contents.get(self.key_name, [])

    def save(self, product: Product):
        self._persist_item(item=product.to_json())
        return product

    def list(self):
        return [make_product(**item) for item in self._read_products()]

    def get(self, product_id):
        products = self._read_products()
        result = [product for product in products if product['product_id'] == product_id]
        return make_product(**result[0])
