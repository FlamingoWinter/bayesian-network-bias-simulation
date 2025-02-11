from typing import TypedDict

from backend.api.responseTypes.recruiterBiasAnalysisResponse.categoricalRecruiterBiasAnalysisResponse import \
    CategoricalRecruiterBiasAnalysisResponse
from backend.api.responseTypes.recruiterBiasAnalysisResponse.continuousRecruiterBiasAnalysisResponse import \
    ContinuousRecruiterBiasAnalysisResponse


class RecruiterBiasAnalysisResponse(TypedDict):
    categoricalBiasAnalysis: CategoricalRecruiterBiasAnalysisResponse
    continuousBiasAnalysis: ContinuousRecruiterBiasAnalysisResponse
