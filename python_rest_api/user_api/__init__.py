from user_api.domain import User


def make_user(**kwargs):
    return User(**kwargs)
