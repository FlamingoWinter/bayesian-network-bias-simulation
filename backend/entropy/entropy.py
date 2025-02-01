import math
from typing import List


def categorical_entropy(probabilities: List[float]):
    return sum([0 if p == 0 else -p * math.log2(p) for p in probabilities])
