import math

import numpy as np


def categorical_entropy_of_probabilities(probabilities: np.ndarray):
    return sum([0 if p == 0 else -p * math.log2(p) for p in probabilities])


def categorical_entropy_of_array(array: np.array):
    _, counts = np.unique(array, return_counts=True)
    probs = counts / len(array)
    return categorical_entropy_of_probabilities(probs)
