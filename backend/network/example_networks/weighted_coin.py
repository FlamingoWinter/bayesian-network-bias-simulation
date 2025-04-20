import numpy as np
import pymc as pm
import xarray as xr

from backend.network.bayesian_network import BayesianNetwork
from backend.network.pymc_network import PyMcNetwork


def get_weighted_coin_network() -> BayesianNetwork:
    with pm.Model() as weighted_coin_model:
        variables = ["p(heads)", "heads_in_100_trials"]
        observed = pm.Data("observed",
                           xr.DataArray(np.zeros(len(variables)), dims=["variable"], coords={"variable": variables}
                                        ))

        p_heads = pm.Uniform("p(heads)", 0, 1, observed=observed["p(heads)"])

        heads_in_100_trials = pm.Binomial("heads_in_100_trials", n=100, p=p_heads,
                                          observed=observed["heads_in_100_trials"])

    weighted_coin_model.name = "weighted_coin"

    weighted_coin_network = PyMcNetwork(weighted_coin_model)

    weighted_coin_network.predefined = True

    return weighted_coin_network
