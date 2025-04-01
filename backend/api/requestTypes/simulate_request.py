from dataclasses import dataclass, field
from typing import List

from backend.utilities.replace_blanks_with_defaults import replace_blanks_with_defaults


@dataclass
class SimulateRequest:
    candidates_to_generate: int = 1_000_000
    train_proportion: float = 0.9
    recruiters: List[str] = field(
        default_factory=lambda: ["random_forest", "logistic_regression",
                                 "shallow_mlp", "deep_mlp",
                                 "transformer", "svm", "bayesian"])
    protected_characteristic: str = ""
    score_threshold: float = 0


def new_simulate_request(**kwargs) -> SimulateRequest:
    kwargs = replace_blanks_with_defaults(kwargs, SimulateRequest)
    return SimulateRequest(**kwargs)
