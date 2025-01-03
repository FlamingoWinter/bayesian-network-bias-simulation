import jsonpickle
import pymc as pm
from django.http import JsonResponse

from backend.network.example_networks.asia import get_asia_network


def get_example_network(request):
    return JsonResponse(jsonpickle.encode(pm.model_to_networkx(get_asia_network())), safe=False)
