import abc

from product_api.domain import Product


class RepoInterface(abc.ABC):
    @abc.abstractmethod
    def save(self, product: Product):
        pass

    def get(self, product_id):
        pass

    def list(self):
        pass

    def delete(self, product_id):
        pass
