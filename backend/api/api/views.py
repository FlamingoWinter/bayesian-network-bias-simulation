from django.core.cache import cache
from django.http import JsonResponse

from backend.api.reponseTypes.conditionResponse import ConditionRequest
from backend.api.reponseTypes.networkResponse import NetworkResponse
from backend.network.bayesian_network import BayesianNetwork


def get_example_network(request):
    network_response: NetworkResponse = cache.get("network-response")

    return JsonResponse(network_response, safe=False)


def condition(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST"}, status=405)
    
    condition_request: ConditionRequest = request.body
    network: BayesianNetwork = cache.get("network")

    condition_response = network.sample_conditioned(condition_request)

    return JsonResponse(condition_response, status=400)
