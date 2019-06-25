from order_api.domain import Order


def make_order(**kwargs):
    return Order(**kwargs)
