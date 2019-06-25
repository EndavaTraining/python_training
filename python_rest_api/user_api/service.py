from user_api.domain import User
from user_api.repo import UserRepo


class UserService:
    def __init__(self):
        self.repo = UserRepo()

    def list(self):
        return self.repo.list()

    def add(self, user: User):
        self.repo.save(user)
        return user.to_json()
