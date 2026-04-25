from dataclasses import asdict, is_dataclass
from typing import Any, Type


def as_dict(obj: Any) -> dict[str, Any]:
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    raise ValueError(f"Error: {obj} not dataclass")


def replace_blanks_with_defaults(
    kwargs: dict[Any, Any], dataclass: Type
) -> dict[Any, Any]:
    for key, default in as_dict(dataclass()).items():
        if (
            kwargs.get(key, default) == ""
            or kwargs.get(key, default) == []
            or kwargs.get(key, default) == [""]
        ):
            kwargs[key] = default
        elif isinstance(default, tuple):
            kwargs[key] = tuple(
                default[i] if item == "" else item for i, item in enumerate(kwargs[key])
            )
    return kwargs
