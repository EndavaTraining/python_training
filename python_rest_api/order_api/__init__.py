import importlib
import os

from order_api.domain import Order

repos = {}


def make_order(**kwargs):
    return Order(**kwargs)


def make_repo():
    repo_type = os.environ.get('repo_type') or 'file'
    if 'order' not in repos:
        module = importlib.import_module(f'order_api.{repo_type}_repo')
        repo = getattr(module, f'Order{repo_type.title()}Repo')()
        repos[f'order_{repo_type}'] = repo
        return repo
    else:
        return repos[f'order_{repo_type}']
