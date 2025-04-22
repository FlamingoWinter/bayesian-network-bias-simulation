from typing import List, Union

from backend.api.responseTypes.network_response import CharacteristicResponse, DistributionType


class Characteristic:
    def __init__(self, name: str, distribution_type: DistributionType):
        self.name: str = name
        self.type: DistributionType = distribution_type
        self.category_names: List[str] = []

    def set_categories(self, category_names):
        self.type = "categorical"
        self.category_names = category_names

    def to_characteristic_response(self, prior_distribution: Union[None, list[float]] = None) -> CharacteristicResponse:
        return {
            'name': self.name,
            'type': self.type,
            'categoryNames': self.category_names,
            'priorDistribution': prior_distribution
        }
