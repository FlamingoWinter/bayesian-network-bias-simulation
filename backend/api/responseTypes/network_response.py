from typing import List, TypedDict, Dict, Union, Literal

type DistributionType = Union[Literal["discrete"], Literal["categorical"], Literal["continuous"]]

CharacteristicResponse = TypedDict('CharacteristicResponse', {
    'name': str,
    'type': DistributionType,
    'categoryNames': List[str],
    'priorDistribution': Union[List[float], None],
})

NetworkResponse = TypedDict('NetworkResponse', {
    'graph': None,
    'scoreCharacteristic': str,
    'applicationCharacteristics': List[str],
    'characteristics': Dict[str, CharacteristicResponse],
    'predefined': bool
})
