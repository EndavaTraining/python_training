import json
from functools import wraps

from order_api import make_order
from order_api.service import OrderService


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


class OrderApi:
    def __init__(self, context):
        self.context = context

    @handle_request()
    def list(self):
        return [order.to_json() for order in OrderService().list()]

    @handle_request()
    def add(self):
        order = self.context
        return OrderService().add(make_order(**order))
