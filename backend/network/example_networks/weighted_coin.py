import pymc as pm

from backend.network.bayesian_network import BayesianNetwork
from backend.visualisation.visualise import visualise_model_as_network


def get_weighted_coin_network() -> BayesianNetwork:
    with pm.Model() as weighted_coin_model:
        p_heads = pm.Uniform("p(heads)", 0, 1)
        # p_heads = pm.TruncatedNormal("p(heads)", mu=0.5, sigma=0.3, lower=0, upper=1)

        heads_in_100_trials = pm.Binomial("heads_in_100_trials", n=100, p=p_heads)

    weighted_coin_model.name = "weighted_coin"

    weighted_coin_network = BayesianNetwork(weighted_coin_model)

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

    return weighted_coin_network


if __name__ == "__main__":
    weighted_coin_network = get_weighted_coin_network()
    visualise_model_as_network(weighted_coin_network.model)
