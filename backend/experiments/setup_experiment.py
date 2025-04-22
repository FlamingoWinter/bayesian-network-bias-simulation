from datetime import datetime

from pgmpy.models import BayesianNetwork as PgBn
from scipy.stats import rv_discrete
from sqlalchemy import Engine

from backend.applicants.applicants import Applicants
from backend.applicants.sample_applicants import sample_applicants
from backend.db.save_to_db import get_engine
from backend.network.generation.assign_cpds import assign_cpds
from backend.network.generation.choose_characteristics import choose_score, choose_protected
from backend.network.generation.generate_dag import generate_random_dag
from backend.network.pgmpy_network import PgmPyNetwork


def setup_experiment() -> tuple[datetime, Engine, PgmPyNetwork, Applicants, str, str]:
    start_time = datetime.now()
    engine: Engine = get_engine()

    graph = generate_random_dag(80, (2, 3))

    category_number_dist = rv_discrete(values=([2, 3, 4], [0.6, 0.3, 0.1]))
    num_categories_by_node: dict[str, int] = {node: category_number_dist.rvs() for node in graph.nodes}

    score_characteristic = choose_score(graph)

    protected_characteristic_name = choose_protected(graph)

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

    applicants: Applicants = sample_applicants(network, 10_000)

    return start_time, engine, network, applicants, score_characteristic, protected_characteristic_name
