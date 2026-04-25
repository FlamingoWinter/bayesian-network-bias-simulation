from typing import Dict, List, Literal, Optional

from pydantic import BaseModel

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
