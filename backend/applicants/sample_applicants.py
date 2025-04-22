import warnings
from typing import cast

import pymc as pm
import xarray as xr
from arviz import InferenceData
from pgmpy.sampling import BayesianModelSampling

from backend.applicants.applicants import Applicants
from backend.network.bayesian_network import BayesianNetwork, num_samples
from backend.network.pgmpy_network import PgmPyNetwork
from backend.utilities.time_function import time_function


class PriorTrace(InferenceData):
    prior: xr.Dataset


@time_function("Generating applicants")
def sample_applicants(network: BayesianNetwork, count: int = num_samples) -> Applicants:
    if network.model_type == "pymc":
        with network.model:
            warnings.simplefilter("ignore", category=RuntimeWarning)
            prior_trace: PriorTrace = cast(PriorTrace, pm.sample_prior_predictive(count))
            warnings.simplefilter("default", category=RuntimeWarning)

        return Applicants(network, prior_trace.prior.to_dataframe())

    if network.model_type == "pgmpy":
        network = cast(network, PgmPyNetwork)
        sampler = BayesianModelSampling(network.model)
        sampled_data = sampler.forward_sample(size=count)

        if network.renaming is None:
            applicants = Applicants(network, sampled_data)
        else:
            applicants = Applicants(network, sampled_data.rename(columns=network.renaming))

        return applicants

    raise "Network is not pgmpy or pymc"
