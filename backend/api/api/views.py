import json

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

from backend.api.cache import from_cache, get_network_from_cache
from backend.api.requestTypes.condition_request import ConditionRequest
from backend.api.responseTypes.bias_response import \
    BiasResponse
from backend.api.responseTypes.network_response import NetworkResponse
from backend.network.bayesian_network import BayesianNetwork
from backend.utilities.time_function import time_function


def get_network(request):
    session_id = request.COOKIES.get('sessionid')
    network_response: NetworkResponse = from_cache(f"network-response_{session_id}", "network-response")
    return JsonResponse(network_response, safe=False)


def get_bias(request):
    session_id = request.COOKIES.get('sessionid')
    bias_response: BiasResponse = from_cache(f"bias_{session_id}")
    return JsonResponse(bias_response, safe=False)


@time_function("Responding to Condition")
def condition(request, predefined=None):
    session_id = request.COOKIES.get('sessionid')
    condition_request: ConditionRequest = json.loads(request.body)
    if predefined is None:
        network: BayesianNetwork = get_network_from_cache(session_id)
    else:
        network: BayesianNetwork = get_network_from_cache(predefined)

    network.condition_on(condition_request)

    try:
        condition_response = network.sample_conditioned()
    except:
        return JsonResponse(status=400)

    return JsonResponse(condition_response, safe=False, status=200)


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'token': get_token(request)})


def session_key(request):
    session_id = request.COOKIES.get('sessionid')

    if not session_id:
        request.session.save()
        session_id = request.session.session_key

    return JsonResponse({'key': session_id})
