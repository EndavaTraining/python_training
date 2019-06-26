import abc

from user_api.domain import User


class RepoInterface(abc.ABC):
    @abc.abstractmethod
    def save(self, user: User):
        pass

    def get(self, user_id):
        pass

    def list(self):
        pass

    def delete(self, user_id):
        pass
