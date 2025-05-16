import random

import networkx as nx


def choose_score(graph: nx.DiGraph, more_than_five_descendants=False) -> str:
    nodes_without_ancestors = [node for node, deg in graph.in_degree() if deg == 0]
    direct_children = list(set([child for p in nodes_without_ancestors for child in graph.successors(p)]))
    direct_grandchildren = list(set([child for p in direct_children for child in graph.successors(p)]))

    score_non_candidates = set(nodes_without_ancestors + direct_children + direct_grandchildren)
    score_candidates = [node for node in graph.nodes if node not in score_non_candidates
                        and (len(nx.descendants(graph, node)) > 5 or not more_than_five_descendants)]

    if len(score_candidates) == 0:
        raise Exception("choose_score failed")
    else:
        score_characteristic = random.sample(score_candidates, 1)[0]
    return score_characteristic


def choose_application(
        graph: nx.DiGraph, condition: int,
        score_characteristic: str, protected_characteristic: str = "",
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
        # 10 Random nodes are selected as application. This doesn't include protected characteristics but includes 5 neighbour characteristics
        proxy_nodes = set(graph.neighbors(protected_characteristic))
        candidate_nodes = [node for node in graph.nodes if
                           node != score_characteristic and node != protected_characteristic and node not in proxy_nodes]
        return random.sample(candidate_nodes, application_size // 2) + random.sample(list(proxy_nodes),
                                                                                     application_size // 2)
    elif condition == 4:
        # 10 Random nodes are selected as application.
        # This doesn't include protected characteristics or any nodes connected by protected characteristic with steps<=2.
        proxy_nodes = set(
            two_hop for one_hop in [protected_characteristic] + list(graph.neighbors(protected_characteristic))
            for two_hop in [one_hop] + list(graph.neighbors(one_hop))
        )
        candidate_nodes = [node for node in graph.nodes if
                           node != score_characteristic and node != protected_characteristic and node not in proxy_nodes]
        return random.sample(candidate_nodes, application_size)


def choose_protected(graph: nx.DiGraph) -> str:
    # Protected characteristic can be any in-node
    nodes_without_ancestors = [node for node, deg in graph.in_degree() if deg == 0]
    return random.sample(nodes_without_ancestors, 1)[0]
