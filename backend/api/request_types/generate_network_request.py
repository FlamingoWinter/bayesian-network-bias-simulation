from typing import Dict, Literal, Tuple, Union

from pydantic import BaseModel, model_validator


class NetworkRequest(BaseModel):
    random_or_predefined: Literal["random"] = "random"
    number_of_nodes: int = 12
    parents_range: Tuple[int, int] = (1, 3)
    mutual_information_range: Tuple[float, float] = (0.1, 0.9)
    values_per_variable: Dict[str, float] = {"2": 0.7, "3": 0.25, "4": 0.05}

    @model_validator(mode="before")
    @classmethod
    def replace_blanks_with_defaults(cls, data: dict) -> dict:
        """Strip empty-string / empty-list sentinels so Pydantic uses field
        defaults.  For tuple-typed fields, replace individual blank elements
        within the list with the corresponding default value."""
        cleaned: dict = {}
        for k, v in data.items():
            if v in ("", [], [""]):
                continue  # omit — Pydantic will fill from the field default
            field = cls.model_fields.get(k)
            default = field.default if field is not None else None
            if isinstance(v, list) and isinstance(default, tuple):
                # Patch blank elements inside tuple-like lists
                cleaned[k] = tuple(
                    default[i] if item == "" else item for i, item in enumerate(v)
                )
            else:
                cleaned[k] = v
        return cleaned


class PredefinedNetworkRequest(BaseModel):
    random_or_predefined: Literal["predefined"]
    predefined_model: str


GenerateNetworkRequest = Union[NetworkRequest, PredefinedNetworkRequest]


def new_random_network_request(**kwargs) -> NetworkRequest:
    kwargs.pop("predefined_model", None)
    return NetworkRequest.model_validate(kwargs)
