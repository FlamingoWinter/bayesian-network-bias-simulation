"""
All Pydantic request and response models for the API.

Request types are used by websocket_consumers/ to parse incoming JSON.
Response types are used by simulation/measure_bias/ and simulation/build_network/
to construct serialisable outputs; see schema.py for pydantic2ts type generation.
"""

from typing import Dict, List, Literal, Optional, Tuple, Union

from pydantic import BaseModel, model_validator

# ── Response types ────────────────────────────────────────────────────────────

DistributionType = Literal["categorical"]


class CharacteristicResponse(BaseModel):
    name: str
    type: DistributionType
    categoryNames: List[str]
    priorDistribution: Optional[List[float]] = None


class NetworkResponse(BaseModel):
    graph: None = None
    scoreCharacteristic: str
    applicationCharacteristics: List[str]
    characteristics: Dict[str, CharacteristicResponse]
    predefined: bool


class GroupPredictionInformationResponse(BaseModel):
    total: int
    hiredAndCompetent: int
    hiredButNotCompetent: int
    notHiredButCompetent: int
    notHiredAndNotCompetent: int

    hired: int
    hiredRate: float
    notHired: int
    notHiredRate: float
    correct: int
    correctRate: float
    incorrect: int
    incorrectRate: float
    competent: int
    competentRate: float
    notCompetent: int
    notCompetentRate: float

    accuracy: float
    falseNegativeRate: float
    falsePositiveRate: float
    falseDiscoveryRate: float
    falseOmissionRate: float


class RecruiterBiasAnalysisResponse(BaseModel):
    general: GroupPredictionInformationResponse
    byGroup: Dict[str, GroupPredictionInformationResponse]


type BiasResponse = Dict[str, RecruiterBiasAnalysisResponse]

ConditionResponse = Dict[str, List[float]]

# ── Request types ─────────────────────────────────────────────────────────────

ConditionRequest = Dict[str, float]


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
                continue
            field = cls.model_fields.get(k)
            default = field.default if field is not None else None
            if isinstance(v, list) and isinstance(default, tuple):
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
