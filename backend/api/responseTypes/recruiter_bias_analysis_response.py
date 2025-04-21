from typing import TypedDict, Dict


class GroupPredictionInformationResponse(TypedDict):
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


class RecruiterBiasAnalysisResponse(TypedDict):
    general: GroupPredictionInformationResponse
    byGroup: Dict[str, GroupPredictionInformationResponse]
