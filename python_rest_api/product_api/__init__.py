from product_api.domain import Product


def make_product(**kwargs):
    return Product(**kwargs)
