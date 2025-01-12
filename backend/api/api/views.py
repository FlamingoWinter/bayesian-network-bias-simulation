from django.core.cache import cache
from django.http import JsonResponse

from backend.api.reponseTypes.networkResponse import NetworkResponse


def get_example_network(request):
    network_response: NetworkResponse = cache.get("network")

    return JsonResponse(network_response, safe=False)
