from typing import List, TypedDict, Dict

NetworkResponse = TypedDict('NetworkResponse', {
    'graph': None,
    'scoreCharacteristic': str,
    'applicationCharacteristics': List[str],
    'descriptionsByCharacteristic': Dict[str, str],
    'description': str
})
