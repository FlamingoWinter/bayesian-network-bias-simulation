import math
from typing import List

import numpy as np


def categorical_entropy(probabilities: List[float]):
    return sum([0 if p == 0 else -p * math.log2(p) for p in probabilities])


def categorical_entropy_of_array(array: np.array):
    _, counts = np.unique(array, return_counts=True)
    probs = counts / len(array)
    return categorical_entropy(probs)
