import importlib
import os

from product_api.domain import Product

repos = {}


def make_product(**kwargs):
    return Product(**kwargs)


def make_repo():
    repo_type = os.environ.get('repo_type') or 'file'
    if 'product' not in repos:
        module = importlib.import_module(f'product_api.{repo_type}_repo')
        repo = getattr(module, f'Product{repo_type.title()}Repo')()
        repos[f'product_{repo_type}'] = repo
        return repo
    else:
        return repos[f'product_{repo_type}']
