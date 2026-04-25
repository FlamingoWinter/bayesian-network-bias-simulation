from typing import Dict, List

from pydantic import BaseModel, model_validator


class SimulateRequest(BaseModel):
    candidates_to_generate: int = 10_000
    train_proportion: float = 0.9
    recruiters: Dict[str, List[str]] = {"random_forest": ["no_mitigation"]}
    protected_characteristic: str = ""
    score_threshold: float = 0

    @model_validator(mode="before")
    @classmethod
    def replace_blanks_with_defaults(cls, data: dict) -> dict:
        """Strip empty-string / empty-list sentinels sent by the frontend so
        Pydantic falls back to the field's declared default instead."""
        return {k: v for k, v in data.items() if v not in ("", [], [""])}


def new_simulate_request(**kwargs) -> SimulateRequest:
    return SimulateRequest.model_validate(kwargs)
