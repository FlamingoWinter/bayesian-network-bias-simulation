from typing import List, TypedDict

DistributionResponse = TypedDict('DistributionResponse', {
    'distribution': List[float],
    'distributionType': str,
    'categoriesForCategoricalDistributions': List[str] | None
})
