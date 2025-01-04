import pymc as pm
from django.http import JsonResponse
from networkx.readwrite.json_graph import node_link_data

from backend.network.example_networks.asia import get_asia_network


def get_example_network(request):
    return JsonResponse(node_link_data(pm.model_to_networkx(get_asia_network())), safe=False)
