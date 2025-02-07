from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork as PgBn

from backend.network.bayesian_network import BayesianNetwork
from backend.network.pgmpy_network import PgmPyNetwork
from backend.visualisation.visualise import visualise_model_as_network


def get_sprinkler_network() -> BayesianNetwork:
    sprinkler_model = PgBn([
        ('cloudy', 'sprinkler'),
        ('cloudy', 'rain'),
        ('sprinkler', 'wet_grass'),
        ('rain', 'wet_grass')
    ])

    cpd_cloudy = TabularCPD(variable='cloudy', variable_card=2, values=[[0.5], [0.5]])
    cpd_sprinkler = TabularCPD(variable='sprinkler', variable_card=2,
                               values=[[0.5, 0.9], [0.5, 0.1]],
                               evidence=['cloudy'], evidence_card=[2])
    cpd_rain = TabularCPD(variable='rain', variable_card=2,
                          values=[[0.8, 0.2], [0.2, 0.8]],
                          evidence=['cloudy'], evidence_card=[2])
    cpd_wet_grass = TabularCPD(variable='wet_grass', variable_card=2,
                               values=[[1.0, 0.7, 0.7, 0.01],
                                       [0.0, 0.3, 0.3, 0.99]],
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

    sprinkler_network.set_description_for_characteristic("cloudy", """
    Whether the weather is cloudy.
    Yes means it is cloudy, No means it is not cloudy.
    """)

    sprinkler_network.set_description_for_characteristic("sprinkler", """
    Whether the sprinkler is on.
    On means the sprinkler is running, Off means it is not.
    """)

    sprinkler_network.set_description_for_characteristic("rain", """
    Whether it is raining.
    Yes means it is raining, No means it is not raining.
    """)

    sprinkler_network.set_description_for_characteristic("wet_grass", """
    Whether the grass is wet.
    Wet means the grass is wet, Dry means it is dry.
    """)

    sprinkler_network.set_description("""
    A simple Bayesian Network describing the probability of grass being wet.
    The presence of clouds influences the likelihood of rain and the sprinkler being turned on (the sprinkler is solar-powered).
    Either rain or the sprinkler being on can cause the grass to be wet.
    """)

    return sprinkler_network


if __name__ == "__main__":
    sprinkler_network = get_sprinkler_network()
    visualise_model_as_network(sprinkler_network.model)
