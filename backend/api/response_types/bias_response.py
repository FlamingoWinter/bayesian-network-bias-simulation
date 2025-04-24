from typing import Dict

from backend.api.response_types.recruiter_bias_analysis_response import \
    RecruiterBiasAnalysisResponse

type BiasResponse = Dict[str, RecruiterBiasAnalysisResponse]
