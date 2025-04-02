from typing import cast

import pymc as pm
from pgmpy.sampling import BayesianModelSampling

from backend.candidates.candidate_group import CandidateGroup
from backend.network.bayesian_network import BayesianNetwork, num_samples
from backend.type_extensions.prior_trace import PriorTrace
from backend.utilities.time_function import time_function


@time_function("Generating candidates")
def generate_candidate_group(network: BayesianNetwork, count: int = num_samples) -> CandidateGroup:
    if network.model_type == "pymc":
        with network.model:
            prior_trace: PriorTrace = cast(PriorTrace, pm.sample_prior_predictive(count))

        candidate_group = CandidateGroup(network, prior_trace.prior.to_dataframe())
        return candidate_group

    if network.model_type == "pgmpy":
        sampler = BayesianModelSampling(network.model)

        sampled_data = sampler.forward_sample(size=count)

        if network.name_mapping is None:
            candidate_group = CandidateGroup(network, sampled_data)
        else:
            candidate_group = CandidateGroup(network, sampled_data.rename(columns=network.name_mapping))

        return candidate_group

    raise "Network is not pgmpy or pymc"
