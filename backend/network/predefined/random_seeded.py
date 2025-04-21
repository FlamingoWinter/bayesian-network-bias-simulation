from backend.network.generation.generate_categorical_network import generate_random_categorical_network
from backend.network.naming_characteristics.name_characteristics import name_characteristics
from backend.network.pgmpy_network import CharacteristicName, PgmPyNetwork


def get_random_seeded_network():
    network: PgmPyNetwork = generate_random_categorical_network(
        20,
        (2, 3),
        (0.6, 0.9),
        seed=967
    )
    network.rename_nodes({c.name: CharacteristicName(
        "Protected Characteristic" if c.name == "0" else
        "Competence" if c.name == "17" else
        "19" if c.name == "19" else c.name, c.category_names)
        for c in network.characteristics.values()})
    return network


def get_named_seeded_network():
    network: PgmPyNetwork = generate_random_categorical_network(
        20,
        (2, 3),
        (0.6, 0.9),
        seed=967
    )
    network.score_characteristic = "19"
    return name_characteristics(network, seed=957)
