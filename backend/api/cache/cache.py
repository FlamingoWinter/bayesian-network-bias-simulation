from typing import Any

import dill
from django.core.cache import cache as django_cache


def cache(key: str, to_cache):
    django_cache.set(key, dill.dumps(to_cache), timeout=None)


def from_cache(key: str) -> Any:
    return dill.loads(django_cache.get(key))
