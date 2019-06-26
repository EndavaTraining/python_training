import importlib
import os

from user_api.domain import User

repos = {}


def make_user(**kwargs):
    return User(**kwargs)


def make_repo():
    repo_type = os.environ.get('repo_type') or 'file'
    repo_key = f'user_{repo_type}'
    if repo_key not in repos:
        module = importlib.import_module(f'user_api.{repo_type}_repo')
        repo = getattr(module, f'User{repo_type.title()}Repo')()
        repos[repo_key] = repo
        return repo
    else:
        return repos[repo_key]
