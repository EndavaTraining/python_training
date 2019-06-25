import uuid


class User:
    def __init__(self, name, user_id=None):
        self.user_id = str(uuid.uuid4()) if user_id is None else user_id
        self.name = name

    def to_json(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
        }
