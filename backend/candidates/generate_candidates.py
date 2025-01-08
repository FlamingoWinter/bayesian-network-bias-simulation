from typing import cast

import pymc as pm

from backend.candidates.candidate_group import CandidateGroup
from backend.network.bayesian_network import BayesianNetwork
from backend.type_extensions.prior_trace import PriorTrace
from backend.utilities.time_function import time_function


@time_function("Generating candidates")
def generate_candidate_group(network: BayesianNetwork, count: int = 10_000) -> CandidateGroup:
    with network.model:
        prior_trace: PriorTrace = cast(PriorTrace, pm.sample_prior_predictive(count))

    candidate_group = CandidateGroup(network, prior_trace.prior.to_dataframe())
    return candidate_group
