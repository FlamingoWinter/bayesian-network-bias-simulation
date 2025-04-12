import random
from typing import Dict

import networkx as nx

from backend.network.pgmpy_network import PgmPyNetwork, CharacteristicName

protected_characteristics = [
    CharacteristicName("Gender", ["Male", "Female", "Non-Binary", "Other"]),
    CharacteristicName("Race", ["White", "Black", "Asian", "Hispanic", "Other"]),
    CharacteristicName("Religion or Belief", ["Christian", "Muslim", "Jewish", "Hindu", "Other"]),
    CharacteristicName("Sexual Orientation", ["Heterosexual", "Homosexual", "Bisexual", "Other"]),
    CharacteristicName("Gender Identity", ["Cisgender", "Transgender", "Non-Binary", "Other"]),
    CharacteristicName("Age", ["18-30", "31-40", "41-50", "51-60", "61+"]),
    CharacteristicName("Marital Status", ["Married", "Single", "Divorced", "Widowed"]),
    CharacteristicName("Family Income Class", ["High Upper Class", "Upper Class", "Middle Class", "Lower Class"]),
    CharacteristicName("School Attended", ["Private", "State", "Selective"]),
]

hide_protected_characteristics = True

intermediary_characteristics = [
    CharacteristicName("Education Opportunities", hml=True),
    CharacteristicName("Work Experience Opportunities", hml=True),
    CharacteristicName("Networking Opportunities", hml=True),
    CharacteristicName("Encouragement to Pursue Job from Family", hml=True),
    CharacteristicName("Encouragement to Pursue Job from Friends", hml=True),
    CharacteristicName("Geographical Mobility", hml=True),
    CharacteristicName("Exposure to Role Models", hml=True),
    CharacteristicName("Confidence in Abilities", hml=True),
    CharacteristicName("Nutritional Access", hml=True),
    CharacteristicName("Healthcare Access", hml=True),
    CharacteristicName("Mental Health Stability", hml=True),
    CharacteristicName("Happiness Within Community", hml=True),
    CharacteristicName("Access to Career Advice", hml=True),
    CharacteristicName("Success on First Impression", hml=True),
    CharacteristicName("Exposure to Threats or Violence", hml=True),
    CharacteristicName("Financial Stability", hml=True),
    CharacteristicName("Pressure of Other Responsibilities", hml=True),
]

affector_characteristics = [
    CharacteristicName("Education", hml=True),
    CharacteristicName("Learning Ability", hml=True),
    CharacteristicName("Cognitive Ability", hml=True),
    CharacteristicName("Interpersonal Skills", hml=True),
    CharacteristicName("Technical Skills", hml=True),
    CharacteristicName("Technical Knowledge", hml=True),
    CharacteristicName("Creative Skills", hml=True),
    CharacteristicName("Analytical Skills", hml=True),
    CharacteristicName("Written Communication Skills", hml=True),
    CharacteristicName("Job Motivation", hml=True),
    CharacteristicName("Conflict Resolution Skills", hml=True),
    CharacteristicName("Leadership Ability", hml=True),
    CharacteristicName("Emotional Intelligence", hml=True),

]

affected_characteristics = [
    CharacteristicName("Interview Performance", hml=True),
    CharacteristicName("Resume Quality", hml=True),
    CharacteristicName("Employee Test Performance", hml=True),
    CharacteristicName("Previous Job Performance", hml=True),
    CharacteristicName("Trial Period Performance", hml=True),
    CharacteristicName("Internship Performance", hml=True),
    CharacteristicName("Commendations from Co-Workers", hml=True),
    CharacteristicName("Job Satisfaction", hml=True),
]

score_characteristic = CharacteristicName("Job Competency", ["Competent", "Not Competent"])


def name_characteristics(network: PgmPyNetwork, seed=None) -> PgmPyNetwork:
    if seed:
        random.seed(seed)
    old_to_new: Dict[str, CharacteristicName] = {}

    graph = network.model.to_directed()

    # 1) Characteristics affected (directly or indirectly) by job competency should be affected_characteristics.
    score_descendants = nx.descendants(graph, network.score_characteristic)
    affected_characteristic_choices = random.sample(affected_characteristics, len(score_descendants))
    for score_descendant, affected_characteristic in zip(score_descendants,
                                                         affected_characteristic_choices):
        old_to_new[score_descendant] = affected_characteristic

    # 2) Characteristics affected by nothing should be protected.
    nodes_without_ancestors = [node for node, deg in graph.in_degree() if deg == 0]
    if hide_protected_characteristics:
        protected_characteristic_choices = [
            CharacteristicName(f"Protected Characteristic {i + 1}", ["1", "2", "3", "4", "5"]) for i in
            range(len(nodes_without_ancestors))]
    else:
        protected_characteristic_choices = random.sample(protected_characteristics, len(nodes_without_ancestors))

    for node_without_ancestor, protected_characteristic in zip(nodes_without_ancestors,
                                                               protected_characteristic_choices):
        old_to_new[node_without_ancestor] = protected_characteristic

    # 3) Direct predecessors of job competency should be affector characteristics

    direct_predecessors = list(graph.predecessors(network.score_characteristic))
    affector_characteristic_choices = random.sample(affector_characteristics, len(direct_predecessors))
    for direct_predecessor, affector_characteristic in zip(direct_predecessors,
                                                           affector_characteristic_choices):
        old_to_new[direct_predecessor] = affector_characteristic

    # 4) Direct Children of Protected Characteristics should be Intermediary
    # Other Characteristics should be Intermediary
    direct_children = list(set([child for p in nodes_without_ancestors for child in graph.successors(p)]))
    unnamed_nodes = [node for node in graph.nodes if node != network.score_characteristic
                     and node not in score_descendants
                     and node not in nodes_without_ancestors
                     and node not in direct_predecessors
                     and node not in direct_children]

    nodes_to_be_intermediary = list(set(direct_children + unnamed_nodes))

    intermediary_characteristic_choices = random.sample(intermediary_characteristics, len(nodes_to_be_intermediary))
    for node_to_be_intermediary, intermediary_characteristic in zip(nodes_to_be_intermediary,
                                                                    intermediary_characteristic_choices):
        old_to_new[node_to_be_intermediary] = intermediary_characteristic

    # 5) Score Characteristic should be job competency.
    old_to_new[network.score_characteristic] = score_characteristic

    # -----------------------------------------------------------------------------------------------------

    for old_name, characteristic_name in old_to_new.items():
        characteristic_name.set_number_values(len(network.characteristics[old_name].category_names))

    network.rename_nodes(old_to_new)
    return network
