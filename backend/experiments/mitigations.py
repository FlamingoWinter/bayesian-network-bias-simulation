from datetime import datetime
from typing import List

from pgmpy.models import BayesianNetwork as PgBn
from scipy.stats import rv_discrete
from sqlalchemy import Engine

from backend.candidates.candidate_group import CandidateGroup
from backend.candidates.generate_candidates import generate_candidate_group
from backend.db.save_to_db import save_run_to_db, save_recruiter_run_to_db, get_engine
from backend.experiments.network_structure_conditions import choose_score_characteristic_modified, \
    choose_protected_characteristic_modfied, choose_application_characteristics_modified
from backend.network.generation.generate_categorical_network import assign_cpds
from backend.network.generation.generate_dag import generate_random_dag
from backend.network.pgmpy_network import PgmPyNetwork
from backend.recruiters.categorical_bias_mitigation.approach_equalised_odds.optimise_for_fnr_and_fpr_equality import \
    OptimiseForFNRAndFPREquality
from backend.recruiters.categorical_bias_mitigation.approach_equalised_odds.optimise_for_fnr_equality import \
    OptimiseForFNREquality
from backend.recruiters.categorical_bias_mitigation.approach_equalised_odds.optimise_for_fnr_fpr_accuracy import \
    OptimiseForFNRFPRAccuracy
from backend.recruiters.categorical_bias_mitigation.approach_equalised_odds.optimise_for_fpr_equality import \
    OptimiseForFPREquality
from backend.recruiters.categorical_bias_mitigation.approach_predictive_parity.optimise_for_fdr_and_for_equality import \
    OptimiseForFDRAndFOREquality
from backend.recruiters.categorical_bias_mitigation.approach_predictive_parity.optimise_for_fdr_equality import \
    OptimiseForFDREquality
from backend.recruiters.categorical_bias_mitigation.approach_predictive_parity.optimise_for_fdr_for_accuracy import \
    OptimiseForFDRFORAccuracy
from backend.recruiters.categorical_bias_mitigation.approach_predictive_parity.optimise_for_for_equality import \
    OptimiseForFOREquality
from backend.recruiters.categorical_bias_mitigation.no_mitigation import NoMitigation
from backend.recruiters.categorical_bias_mitigation.satisfy_demographic_parity import SatisfyDemographicParity
from backend.recruiters.categorical_bias_mitigation.satisfy_proportional_parity import SatisfyProportionalParity
from backend.recruiters.categorical_output.random_forest_recruiter import RandomForestRecruiter
from backend.recruiters.recruiter import Recruiter
from backend.simulate import simulate
from backend.utilities.time_function import time_function

category_number_dist = rv_discrete(values=([2, 3, 4], [0.6, 0.3, 0.1]))


@time_function("Network Structure Conditions Run")
def mitigations():
    start_time = datetime.now()
    engine: Engine = get_engine()

    parents_range = (2, 3)
    category_number_dist = rv_discrete(values=([2, 3, 4], [0.6, 0.3, 0.1]))

    graph = generate_random_dag(80, parents_range[0], parents_range[1])
    num_categories_by_node: dict[str, int] = {node: category_number_dist.rvs() for node in graph.nodes}

    try:
        score_characteristic = choose_score_characteristic_modified(graph)
    except:
        return mitigations()

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

    network.application_characteristics = choose_application_characteristics_modified(
        graph, 1, score_characteristic, protected_characteristic_name)

    recruiters: List[Recruiter] = [
        RandomForestRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity(),
             OptimiseForFNRFPRAccuracy(), OptimiseForFNRAndFPREquality(), OptimiseForFNREquality(),
             OptimiseForFPREquality(),
             OptimiseForFDRFORAccuracy(), OptimiseForFDRAndFOREquality(), OptimiseForFDREquality(),
             OptimiseForFOREquality(),
             ]),
    ]

    protected_characteristic = network.characteristics[protected_characteristic_name]
    bias_by_recruiter = simulate(candidate_group, recruiters, protected_characteristic)

    db_run_id = save_run_to_db(engine, network, candidate_group, protected_characteristic_name, 5,
                               datetime.now() - start_time)
    for bias, recruiter_bias_analysis in bias_by_recruiter.items():
        recruiter_run_id = save_recruiter_run_to_db(engine, db_run_id, recruiter_bias_analysis)


if __name__ == "__main__":
    mitigations()
