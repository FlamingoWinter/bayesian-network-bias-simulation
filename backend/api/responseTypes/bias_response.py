from typing import Dict

from backend.api.responseTypes.recruiter_bias_analysis_response import \
    RecruiterBiasAnalysisResponse

type BiasResponse = Dict[str, RecruiterBiasAnalysisResponse]
