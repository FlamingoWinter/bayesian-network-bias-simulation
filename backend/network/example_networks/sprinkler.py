from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork as PgBn

from backend.network.bayesian_network import BayesianNetwork
from backend.network.pgmpy_network import PgmPyNetwork


def get_sprinkler_network() -> BayesianNetwork:
    sprinkler_model = PgBn([
        ('cloudy', 'sprinkler'),
        ('cloudy', 'rain'),
        ('sprinkler', 'wet_grass'),
        ('rain', 'wet_grass')
    ])

    cpd_cloudy = TabularCPD(variable='cloudy', variable_card=2, values=[[0.5], [0.5]])
    cpd_sprinkler = TabularCPD(variable='sprinkler', variable_card=2,
                               values=[[0.5, 0.95], [0.5, 0.05]],
                               evidence=['cloudy'], evidence_card=[2])
    cpd_rain = TabularCPD(variable='rain', variable_card=2,
                          values=[[0.7, 0.0], [0.3, 1.0]],
                          evidence=['cloudy'], evidence_card=[2])
    cpd_wet_grass = TabularCPD(variable='wet_grass', variable_card=2,
                               values=[[1.0, 1.0, 1.0, 0.1],
                                       [0.0, 0.0, 0.0, 0.9]],
                               evidence=['sprinkler', 'rain'], evidence_card=[2, 2])

    sprinkler_model.add_cpds(cpd_cloudy, cpd_sprinkler, cpd_rain, cpd_wet_grass)

    if not sprinkler_model.check_model():
        raise ValueError("The Bayesian Network is not valid!")

    sprinkler_model.name = "sprinkler"

    sprinkler_network = PgmPyNetwork(sprinkler_model,
                                     "wet_grass",
                                     ["sprinkler", "rain"])

    sprinkler_network.set_category_names_for_characteristic("cloudy", ['Yes', 'No'])
    sprinkler_network.set_category_names_for_characteristic("sprinkler", ['On', 'Off'])
    sprinkler_network.set_category_names_for_characteristic("rain", ['Yes', 'No'])
    sprinkler_network.set_category_names_for_characteristic("wet_grass", ['Wet', 'Dry'])

    sprinkler_network.predefined = True

    return sprinkler_network
