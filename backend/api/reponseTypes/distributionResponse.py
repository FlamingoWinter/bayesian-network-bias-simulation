from typing import List, TypedDict

DistributionResponse = TypedDict('DistributionResponse', {
    'distribution': List[float],
    'isCategoricalVariable': bool,
    'categoriesForCategoricalDistributions': List[str] | None
})
