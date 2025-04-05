import random
from datetime import datetime
from typing import List

import networkx as nx
from pgmpy.models import BayesianNetwork as PgBn
from scipy.stats import rv_discrete
from sqlalchemy import Engine

from backend.candidates.candidate_group import CandidateGroup
from backend.candidates.generate_candidates import generate_candidate_group
from backend.db.save_to_db import save_run_to_db, save_recruiter_run_to_db, get_engine
from backend.network.generation.generate_categorical_network import assign_cpds
from backend.network.generation.generate_dag import generate_random_dag
from backend.network.pgmpy_network import PgmPyNetwork
from backend.recruiters.categorical_bias_mitigation.no_mitigation import NoMitigation
from backend.recruiters.categorical_bias_mitigation.satisfy_demographic_parity import SatisfyDemographicParity
from backend.recruiters.categorical_bias_mitigation.satisfy_proportional_parity import SatisfyProportionalParity
from backend.recruiters.categorical_output.bayesian_recruiter import BayesianRecruiter
from backend.recruiters.categorical_output.deep_mlp_recruiter import DeepMLPRecruiter
from backend.recruiters.categorical_output.encoder_only_transformer_recruiter import EncoderOnlyTransformerRecruiter
from backend.recruiters.categorical_output.logistic_regression_recruiter import LogisticRegressionRecruiter
from backend.recruiters.categorical_output.random_forest_recruiter import RandomForestRecruiter
from backend.recruiters.categorical_output.shallow_mlp_recruiter import ShallowMLPRecruiter
from backend.recruiters.categorical_output.svm_recruiter import SVMRecruiter
from backend.recruiters.recruiter import Recruiter
from backend.simulate import simulate
from backend.utilities.time_function import time_function

category_number_dist = rv_discrete(values=([2, 3, 4], [0.6, 0.3, 0.1]))


@time_function("Network Structure Conditions Run")
def network_structure_conditions_run():
    start_time = datetime.now()
    engine: Engine = get_engine()

    parents_range = (2, 3)
    category_number_dist = rv_discrete(values=([2, 3, 4], [0.6, 0.3, 0.1]))

    graph = generate_random_dag(80, parents_range[0], parents_range[1])
    num_categories_by_node: dict[str, int] = {node: category_number_dist.rvs() for node in graph.nodes}

    try:
        score_characteristic = choose_score_characteristic_modified(graph)
    except:
        return network_structure_conditions_run()

    protected_characteristic_name = choose_protected_characteristic_modfied(graph)

    num_categories_by_node[score_characteristic] = 2
    num_categories_by_node[protected_characteristic_name] = 2

    model = PgBn(ebunch=graph)
    assign_cpds(model, graph, num_categories_by_node)

    network: PgmPyNetwork = PgmPyNetwork(model)

    for node in graph.nodes:
        network.set_category_names_for_characteristic(node, [str(x) for x in
                                                             list(range(1, num_categories_by_node[node] + 1))])

    network.score_characteristic = score_characteristic
    network.predefined = False

    candidate_group: CandidateGroup = generate_candidate_group(network, 10_000)

    network_creation_time = datetime.now()

    for condition in [1, 2, 3, 4]:
        condition_start_time = datetime.now()
        network.application_characteristics = choose_application_characteristics_modified(
            graph, condition, score_characteristic, protected_characteristic_name)

        recruiters: List[Recruiter] = [
            RandomForestRecruiter(
                [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
            BayesianRecruiter(
                [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
            ShallowMLPRecruiter(
                [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
            DeepMLPRecruiter(
                [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
            EncoderOnlyTransformerRecruiter(
                [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
            LogisticRegressionRecruiter(
                [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
            SVMRecruiter(
                [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        ]

        protected_characteristic = network.characteristics[protected_characteristic_name]
        bias_by_recruiter = simulate(candidate_group, recruiters, protected_characteristic)

        db_run_id = save_run_to_db(engine, network, candidate_group, protected_characteristic_name, condition,
                                   datetime.now() - condition_start_time + network_creation_time - start_time)
        for bias, recruiter_bias_analysis in bias_by_recruiter.items():
            recruiter_run_id = save_recruiter_run_to_db(engine, db_run_id, recruiter_bias_analysis)

        # TODO: Remove
        # print_bias_summary(bias_by_recruiter)


def choose_application_characteristics_modified(
        graph: nx.DiGraph, condition: int,
        score_characteristic: str, protected_characteristic: str,
        application_size: int = 10) -> str:
    if condition == 1:
        # 10 Random nodes are selected as application. This doesn't include protected Characteristic.
        candidate_nodes = [node for node in graph.nodes if
                           node != score_characteristic and node != protected_characteristic]
        return random.sample(candidate_nodes, application_size)
    elif condition == 2:
        # 10 Random nodes are selected as application. This includes protected Characteristic.
        candidate_nodes = [node for node in graph.nodes if
                           node != score_characteristic and node != protected_characteristic]
        return random.sample(candidate_nodes, application_size - 1) + [protected_characteristic]
    elif condition == 3:
        # 10 Random nodes are selected as application.
        # This doesn't include protected characteristics or any nodes connected by protected characteristic with steps<=2.
        direct_children = list(graph.successors(protected_characteristic))
        direct_grandchildren = list(set([child for p in direct_children for child in graph.successors(p)]))
        candidate_nodes = [node for node in graph.nodes if node != score_characteristic
                           and node != protected_characteristic
                           and node not in direct_children
                           and node not in direct_grandchildren]
        return random.sample(candidate_nodes, application_size)
    elif condition == 4:
        # 10 random descendants of score are selected as application.
        candidate_nodes = nx.descendants(graph, score_characteristic)
        return random.sample(list(candidate_nodes), application_size)


def choose_protected_characteristic_modfied(graph: nx.DiGraph) -> str:
    # Protected characteristic can be any in-node
    nodes_without_ancestors = [node for node, deg in graph.in_degree() if deg == 0]
    return random.sample(nodes_without_ancestors, 1)[0]


def choose_score_characteristic_modified(graph: nx.DiGraph) -> str:
    # Score cannot be a child or grandchild of an in-node. Score characteristic must have at least 20 descendants.
    nodes_without_ancestors = [node for node, deg in graph.in_degree() if deg == 0]
    direct_children = list(set([child for p in nodes_without_ancestors for child in graph.successors(p)]))
    direct_grandchildren = list(set([child for p in direct_children for child in graph.successors(p)]))

    score_non_candidates = set(nodes_without_ancestors + direct_children + direct_grandchildren)
    score_candidates = [node for node in graph.nodes if
                        node not in score_non_candidates and len(nx.descendants(graph, node)) > 20]

    if len(score_candidates) == 0:
        raise "Error - Couldn't assign score"
    else:
        score_characteristic = random.sample(score_candidates, 1)[0]
    return score_characteristic


if __name__ == "__main__":
    # while True:
    #     try:
    network_structure_conditions_run()
# except:
#     pass
