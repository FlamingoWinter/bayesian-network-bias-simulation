import json

import numpy as np
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

from backend.api.cache.cache import from_cache
from backend.api.responseTypes.conditionResponse import ConditionRequest
from backend.api.responseTypes.networkResponse import NetworkResponse
from backend.network.bayesian_network import BayesianNetwork
from backend.network.generate_network import generate_network
from backend.utilities.time_function import time_function


def get_example_network(request):
    network_response: NetworkResponse = from_cache("network-response")

    return JsonResponse(network_response, safe=False)


@time_function("Responding to Condition")
def condition(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST"}, status=405)

    condition_request: ConditionRequest = json.loads(request.body)
    network: BayesianNetwork = from_cache("network")

    network.model = generate_network(
        {characteristic: np.array([value]) for characteristic, value in condition_request.items()}).model
    if network.model_type == "pgmpy":
        network.observed = condition_request

    try:
        condition_response = network.sample_conditioned()
    except:
        return JsonResponse(status=400)

    return JsonResponse(condition_response, safe=False, status=200)


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'token': get_token(request)})
