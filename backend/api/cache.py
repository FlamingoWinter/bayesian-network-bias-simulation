from typing import Any

import dill
from django.core.cache import cache as django_cache


def cache(key: str, to_cache):
    django_cache.set(key, dill.dumps(to_cache), timeout=None)


def from_cache(key: str, backup_key: str) -> Any:
    try:
        return dill.loads(django_cache.get(key))
    except:
        print("used backup instead of", key)
        return dill.loads(django_cache.get(backup_key))
