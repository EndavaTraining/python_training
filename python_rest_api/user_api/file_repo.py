import json

from user_api import make_user
from user_api.domain import User
from user_api.repo import RepoInterface


class UserFileRepo(RepoInterface):
    def __init__(self):
        self.file_name = 'database.json'
        self.key_name = 'users'

    def _persist_item(self, item):
        with open(self.file_name) as file_content:
            current_data = json.load(file_content)

        current_data_users = current_data.get(self.key_name, [])
        current_data_users.append(item)
        current_data[self.key_name] = current_data_users

        with open(self.file_name, 'w') as file:
            json.dump(current_data, file)

    def _read_users(self):
        with open(self.file_name) as file_content:
            file_contents = json.load(file_content)
            return file_contents.get(self.key_name, [])

    def save(self, user: User):
        self._persist_item(item=user.to_json())
        return user

    def list(self):
        return [make_user(**item) for item in self._read_users()]
