from typing import List, TypedDict, Dict, Literal, Union

type DistributionType = Literal["categorical"]

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
