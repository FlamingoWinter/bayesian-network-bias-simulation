from typing import Union, Literal

from backend.network.generation.generate_categorical_network import generate_random_categorical_network
from backend.utilities.time_function import time_function


@time_function("Generating random network")
def generate_random_network(nodes: int):
    categorical_or_continuous: Union[Literal["categorical"], Literal["continuous"]]

    return generate_random_categorical_network(nodes)
