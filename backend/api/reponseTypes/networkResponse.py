from typing import List, TypedDict, Dict, Union, Literal

type DistributionType = Union[Literal["discrete"], Literal["categorical"], Literal["continuous"]]

CharacteristicResponse = TypedDict('CharacteristicResponse', {
    'name': str,
    'description': str,
    'type': DistributionType,
    'categoryNames': List[str]
})

NetworkResponse = TypedDict('NetworkResponse', {
    'graph': None,
    'scoreCharacteristic': str,
    'applicationCharacteristics': List[str],
    'characteristics': Dict[str, CharacteristicResponse],
    'description': str
})
