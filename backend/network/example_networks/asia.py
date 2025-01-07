import numpy as np
import pymc as pm
import pytensor as pt

from backend.network.bayesian_network import BayesianNetwork
from backend.visualisation.visualise import visualise_model_as_network


# Transcribed from https://www.bnlearn.com/bnrepository/discrete-small.html#asia

def get_asia_network() -> BayesianNetwork:
    def p_asia():
        return [0.01, 0.99]

    def p_tub(asia):
        return pt.shared(np.asarray([[0.05, 0.95], [0.01, 0.99]])
                         )[asia]

    def p_smoke():
        return [0.5, 0.5]

    def p_lung(smoke):
        return pt.shared(np.asarray([[0.1, 0.9], [0.01, 0.99]])
                         )[smoke]

    def p_bronc(smoke):
        return pt.shared(np.asarray([[0.6, 0.4], [0.3, 0.7]])
                         )[smoke]

    def p_either(lung, tub):
        return pt.shared(np.asarray([
            [[1.0, 0.0], [1.0, 0.0]],
            [[1.0, 0.0], [0.0, 1.0]]
        ]))[lung, tub]

    def p_xray(either):
        return pt.shared(np.asarray([[0.98, 0.2], [0.05, 0.95]])
                         )[either]

    def p_dysp(bronc, either):
        return pt.shared(np.asarray([
            [[0.9, 0.1], [0.7, 0.3]],
            [[0.8, 0.2], [0.1, 0.9]]
        ]))[bronc, either]

    with pm.Model() as asia_network:
        asia = pm.Categorical('asia', p_asia())
        tub = pm.Categorical('tub', p_tub(asia))
        smoke = pm.Categorical('smoke', p_smoke())
        lung = pm.Categorical('lung', p_lung(smoke))
        bronc = pm.Categorical('bronc', p_bronc(smoke))
        either = pm.Categorical('either', p_either(lung, tub))
        xray = pm.Categorical('xray', p_xray(either))
        dysp = pm.Categorical('dysp', p_dysp(bronc, either))

    return BayesianNetwork(asia_network, "dysp", ["either", "bronc"],
                           {
                               'asia': ['True', 'False'],
                               'tub': ['Positive', 'Negative'],
                               'smoke': ['Yes', 'No'],
                               'lung': ['Present', 'Absent'],
                               'bronc': ['Present', 'Absent'],
                               'either': ['Present', 'Absent'],
                               'xray': ['Positive', 'Negative'],
                               'dysp': ['Present', 'Absent'],
                           })


if __name__ == "__main__":
    asia_network = get_asia_network()
    visualise_model_as_network(asia_network)
