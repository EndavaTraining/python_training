from user_api.domain import User
from user_api import make_repo


class UserService:
    def __init__(self):
        self.repo = make_repo()

    def list(self):
        return self.repo.list()

    def add(self, user: User):
        self.repo.save(user)
        return user.to_json()
