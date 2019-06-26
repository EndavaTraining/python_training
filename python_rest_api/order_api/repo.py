import abc

from order_api.domain import Order


class RepoInterface(abc.ABC):
    @abc.abstractmethod
    def save(self, order: Order):
        pass

    def get(self, order_id):
        pass

    def list(self):
        pass

    def delete(self, order_id):
        pass
