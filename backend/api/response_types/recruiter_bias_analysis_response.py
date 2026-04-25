from typing import Dict

from pydantic import BaseModel


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
