import json
from functools import wraps

from user_api import make_user
from user_api.service import UserService


def response(message, status_code):
    return {
        'status_code': str(status_code),
        'body': json.dumps(message)
    }


def handle_request():
    """
    Handle common exceptions.
    :return: Decorated function.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return response(f(*args, *kwargs), 200)
            except ValueError as e:
                return response(str(e), 412)
            except KeyError as e:
                return response(str(e), 412)

        return wrapper

    return decorator


class UserApi:
    def __init__(self, context):
        self.context = context

    @handle_request()
    def list(self):
        return [user.to_json() for user in UserService().list()]

    @handle_request()
    def add(self):
        user = self.context
        return UserService().add(make_user(**user))
