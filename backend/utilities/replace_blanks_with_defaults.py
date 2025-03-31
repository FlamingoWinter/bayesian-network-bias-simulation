from dataclasses import is_dataclass, asdict
from typing import Type


def as_dict(obj: any) -> dict[str, any]:
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    raise f"Error: {obj} not dataclass"


def replace_blanks_with_defaults(kwargs: dict[any, any], dataclass: Type) -> dict[any, any]:
    for key, default in as_dict(dataclass()).items():
        if kwargs.get(key, default) == "" or kwargs.get(key, default) == [] or kwargs.get(key, default) == [""]:
            kwargs[key] = default
        elif isinstance(default, tuple):
            kwargs[key] = tuple(default[i] if item == "" else item for i, item in enumerate(kwargs[key]))
    return kwargs
