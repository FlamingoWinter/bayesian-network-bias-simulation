from typing import Dict

import numpy as np
import pymc as pm
import pytensor as pt

from backend.network.bayesian_network import BayesianNetwork
from backend.visualisation.visualise import visualise_model_as_network


# Transcribed from https://www.bnlearn.com/bnrepository/discrete-small.html#asia

def get_asia_network(observed: Dict[str, np.array]) -> BayesianNetwork:
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

    with pm.Model() as asia_model:
        asia = pm.Categorical('asia', p_asia(), observed=observed.get('asia', None))
        tub = pm.Categorical('tub', p_tub(asia), observed=observed.get('tub', None))
        smoke = pm.Categorical('smoke', p_smoke(), observed=observed.get('smoke', None))
        lung = pm.Categorical('lung', p_lung(smoke), observed=observed.get('lung', None))
        bronc = pm.Categorical('bronc', p_bronc(smoke), observed=observed.get('bronc', None))
        either = pm.Categorical('either', p_either(lung, tub), observed=observed.get('either', None))
        xray = pm.Categorical('xray', p_xray(either), observed=observed.get('xray', None))
        dysp = pm.Categorical('dysp', p_dysp(bronc, either), observed=observed.get('dysp', None))

    asia_model.name = "asia"

    asia_network = BayesianNetwork(asia_model, "dysp", ["either", "bronc"])

    asia_network.set_category_names_for_characteristic("asia", ['True', 'False'])
    asia_network.set_category_names_for_characteristic("tub", ['Positive', 'Negative'])
    asia_network.set_category_names_for_characteristic("smoke", ['Yes', 'No'])
    asia_network.set_category_names_for_characteristic("lung", ['Present', 'Absent'])
    asia_network.set_category_names_for_characteristic("bronc", ['Present', 'Absent'])
    asia_network.set_category_names_for_characteristic("either", ['Present', 'Absent'])
    asia_network.set_category_names_for_characteristic("xray", ['Positive', 'Negative'])
    asia_network.set_category_names_for_characteristic("dysp", ['Present', 'Absent'])

    asia_network.set_description_for_characteristic("asia", """
    Whether a person has visited Asia recently.
    True means the person has visited Asia recently. False means the person has not visited Asia recently.
    """)

    asia_network.set_description_for_characteristic("tub", """
        Whether a person has tuberculosis.
        Positive means the person has tuberculosis. Negative means they do not have tuberculosis.
    """)

    asia_network.set_description_for_characteristic("smoke", """
        Whether a person smokes.
        Yes means the person smokes. No means they do not smoke.
    """)

    asia_network.set_description_for_characteristic("lung", """
        Whether a person has lung cancer.
        Present means the person has lung cancer. Absent means they do not have lung cancer.
    """)

    asia_network.set_description_for_characteristic("bronc", """
        Whether a person has bronchitis.
        Present means the person has bronchitis. Absent means they do not have bronchitis.
    """)

    asia_network.set_description_for_characteristic("either", """
        Whether a person has either bronchitis or lung cancer.
        Present means the person has either bronchitis or lung cancer. Absent means they have neither bronchitis nor lung cancer.
    """)

    asia_network.set_description_for_characteristic("xray", """
        Whether a person's chest X-ray shows any abnormality.
        Positive means the X-ray shows an abnormality. Negative means the X-ray does not show any abnormality.
    """)

    asia_network.set_description_for_characteristic("dysp", """
        Whether a person experiences dyspnea (shortness of breath).
        Present means the person experiences shortness of breath. Absent means they do not experience shortness of breath.
    """)

    asia_network.set_description("""
    An example network given by Lauritzen and Spigelhalter (1988)
    Whether a person has been to asia is likely to affect whether they have tuberculosis, as incidence of tuberculosis was higher in Asia at the time.
    Whether a person smoke's may be indicative of lung cancer or bronchitis and either of these features may affect shortness of breath.
    The presence of lung cancer or tuberculosis may be identified by an x-ray, but the presence of bronchitis will not be.
    """)

    return asia_network


if __name__ == "__main__":
    asia_network = get_asia_network()
    visualise_model_as_network(asia_network.model)
