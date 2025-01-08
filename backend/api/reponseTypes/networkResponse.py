from typing import List, TypedDict

NetworkResponse = TypedDict('NetworkResponse', {
    'network': None,
    'scoreCharacteristic': str,
    'applicationCharacteristics': List[str]
})
