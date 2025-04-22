from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork as PgBn

from backend.network.pgmpy_network import PgmPyNetwork


def get_shark_sighting_network() -> PgmPyNetwork:
    shark_model = PgBn([
        ('hot_weather', 'ice_cream_sales'),
        ('hot_weather', 'beach_visits'),
        ('beach_visits', 'shark_sightings'),
        ('beach_visits', 'ice_cream_sales')
    ])

    cpd_hot_weather = TabularCPD(variable='hot_weather', variable_card=2, values=[[0.5], [0.5]])
    cpd_beach_visits = TabularCPD(variable='beach_visits', variable_card=2,
                                  values=[[0.85, 0.05], [0.15, 0.95]],
                                  evidence=['hot_weather'], evidence_card=[2])
    cpd_ice_cream_sales = TabularCPD(variable='ice_cream_sales', variable_card=2,
                                     values=[
                                         [0.95, 0.85, 0.6, 0.2],
                                         [0.05, 0.15, 0.4, 0.8]
                                     ],
                                     evidence=['hot_weather', 'beach_visits'],
                                     evidence_card=[2, 2]
                                     )

    cpd_shark_sightings = TabularCPD(variable='shark_sightings', variable_card=2,
                                     values=[[0.95, 0.1], [0.05, 0.9]],
                                     evidence=['beach_visits'], evidence_card=[2])

    shark_model.add_cpds(cpd_hot_weather, cpd_ice_cream_sales, cpd_beach_visits, cpd_shark_sightings)

    shark_model.name = "shark_sightings"

    shark_network = PgmPyNetwork(shark_model,
                                 "shark_sightings",
                                 ["ice_cream_sales", "beach_visits"])

    shark_network.set_category_names_for_characteristic("hot_weather", ['Yes', 'No'])
    shark_network.set_category_names_for_characteristic("ice_cream_sales", ['High', 'Low'])
    shark_network.set_category_names_for_characteristic("beach_visits", ['Many', 'Few'])
    shark_network.set_category_names_for_characteristic("shark_sightings", ['Yes', 'No'])

    shark_network.predefined = True

    return shark_network
