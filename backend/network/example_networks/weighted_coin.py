import numpy as np
import pymc as pm
import xarray as xr

from backend.network.bayesian_network import BayesianNetwork
from backend.network.pymc_network import PyMcNetwork
from backend.visualisation.visualise import visualise_model_as_network


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

    weighted_coin_network.set_description_for_characteristic("p(heads)", """
        The probability of the weighted coin landing heads side up.
    """)

    weighted_coin_network.set_description_for_characteristic("heads_in_100_trials", """
        The number of observed heads after flipping the coin 100 times.
    """)

    weighted_coin_network.set_description("""
        A coin is known to be weighted but the probability of it landing heads isn't known. 
        A (possibly naive) uniform prior is used, and the weighting can be estimated from the result of 100 coin flips.
    """)

    weighted_coin_network.predefined = True

    return weighted_coin_network


if __name__ == "__main__":
    weighted_coin_network = get_weighted_coin_network()
    visualise_model_as_network(weighted_coin_network.model)
