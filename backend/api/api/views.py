import json

import pymc as pm
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from pgmpy.models import BayesianNetwork as PgBn

from backend.api.cache.cache import from_cache
from backend.api.responseTypes.conditionResponse import ConditionRequest
from backend.api.responseTypes.networkResponse import NetworkResponse
from backend.api.responseTypes.recruiterBiasAnalysisResponse.biasResponse import \
    BiasResponse
from backend.network.bayesian_network import BayesianNetwork
from backend.utilities.time_function import time_function


def get_example_network(request):
    network_response: NetworkResponse = from_cache(f"network-response_{request.session.session_key}",
                                                   "network-response")

    return JsonResponse(network_response, safe=False)


def get_bias(request):
    bias_response: BiasResponse = from_cache(f"bias_{request.session.session_key}", "")

    return JsonResponse(bias_response, safe=False)


@time_function("Responding to Condition")
def condition(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST"}, status=405)

    condition_request: ConditionRequest = json.loads(request.body)
    network: BayesianNetwork = from_cache(f"network_{request.session.session_key}",
                                          "network")
    if network.model_type == "pgmpy":
        network.model.__class__ = PgBn
    else:
        network.model.__class__ = pm.Model

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
    session_key = request.session.session_key

    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    return JsonResponse({'key': session_key})
