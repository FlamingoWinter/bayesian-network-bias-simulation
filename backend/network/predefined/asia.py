from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork as PgBn

from backend.network.bayesian_network import BayesianNetwork
from backend.network.pgmpy_network import PgmPyNetwork


# Transcribed from https://www.bnlearn.com/bnrepository/discrete-small.html#asia

def get_asia_network() -> BayesianNetwork:
    asia_model = PgBn([
        ('asia', 'tub'),
        ('smoke', 'lung'),
        ('smoke', 'bronc'),
        ('lung', 'either'),
        ('tub', 'either'),
        ('either', 'xray'),
        ('either', 'dysp'),
        ('bronc', 'dysp')
    ])

    cpd_asia = TabularCPD(variable='asia', variable_card=2, values=[[0.01], [0.99]])
    cpd_tub = TabularCPD(variable='tub', variable_card=2,
                         values=[[0.05, 0.01], [0.95, 0.99]],
                         evidence=['asia'], evidence_card=[2])
    cpd_smoke = TabularCPD(variable='smoke', variable_card=2, values=[[0.5], [0.5]])
    cpd_lung = TabularCPD(variable='lung', variable_card=2,
                          values=[[0.1, 0.01], [0.9, 0.99]],
                          evidence=['smoke'], evidence_card=[2])
    cpd_bronc = TabularCPD(variable='bronc', variable_card=2,
                           values=[[0.6, 0.3], [0.4, 0.7]],
                           evidence=['smoke'], evidence_card=[2])
    cpd_either = TabularCPD(variable='either', variable_card=2,
                            values=[
                                [1.0, 1.0, 1.0, 0.0],
                                [0.0, 0.0, 0.0, 1.0]
                            ],
                            evidence=['lung', 'tub'], evidence_card=[2, 2])
    cpd_xray = TabularCPD(variable='xray', variable_card=2,
                          values=[[0.98, 0.05], [0.02, 0.95]],
                          evidence=['either'], evidence_card=[2])
    cpd_dysp = TabularCPD(variable='dysp', variable_card=2,
                          values=[
                              [0.9, 0.7, 0.8, 0.1],
                              [0.1, 0.3, 0.2, 0.9]
                          ],
                          evidence=['bronc', 'either'], evidence_card=[2, 2])

    asia_model.add_cpds(cpd_asia, cpd_tub, cpd_smoke, cpd_lung, cpd_bronc, cpd_either, cpd_xray, cpd_dysp)

    if not asia_model.check_model():
        raise ValueError("The Bayesian Network is not valid!")

    asia_model.name = "asia"

    asia_network = PgmPyNetwork(asia_model,
                                "dysp",
                                ["either", "bronc"])

    asia_network.set_category_names_for_characteristic("asia", ['Yes', 'No'])
    asia_network.set_category_names_for_characteristic("tub", ['Present', 'Absent'])
    asia_network.set_category_names_for_characteristic("smoke", ['Yes', 'No'])
    asia_network.set_category_names_for_characteristic("lung", ['Present', 'Absent'])
    asia_network.set_category_names_for_characteristic("bronc", ['Present', 'Absent'])
    asia_network.set_category_names_for_characteristic("either", ['Present', 'Absent'])
    asia_network.set_category_names_for_characteristic("xray", ['Abnormal', 'Normal'])
    asia_network.set_category_names_for_characteristic("dysp", ['Present', 'Absent'])

    asia_network.predefined = True

    return asia_network
