import json

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

from backend.api.cache import from_cache, get_network_from_cache
from backend.api.schemas import ConditionRequest
from backend.api.schemas import BiasResponse
from backend.api.schemas import NetworkResponse
from backend.simulation.build_network.bayesian_network import BayesianNetwork
from backend.utils.time_function import time_function


def get_network(request):
    session_id = request.COOKIES.get("sessionid")
    network_response: NetworkResponse = from_cache(
        f"network-response_{session_id}", "network-response"
    )
    return JsonResponse(network_response.model_dump())


def get_bias(request):
    session_id = request.COOKIES.get("sessionid")
    bias_response: BiasResponse = from_cache(f"bias_{session_id}")
    # bias_response values may be Pydantic models; serialise them to plain dicts
    serialised = {
        recruiter: {
            mitigation: analysis.model_dump()
            for mitigation, analysis in mitigations.items()
        }
        for recruiter, mitigations in bias_response.items()
    }
    return JsonResponse(serialised)


@time_function("Responding to Condition")
def condition(request, predefined=None):
    session_id = request.COOKIES.get("sessionid")
    condition_request: ConditionRequest = json.loads(request.body)
    if predefined is None:
        network: BayesianNetwork = get_network_from_cache(session_id)
    else:
        network: BayesianNetwork = get_network_from_cache(predefined)

    network.condition_on(condition_request)

    try:
        condition_response = network.sample_conditioned()
    except Exception:
        return JsonResponse({}, status=400)

    return JsonResponse(condition_response, safe=False, status=200)


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"token": get_token(request)})


def session_key(request):
    session_id = request.COOKIES.get("sessionid")

    if not session_id:
        request.session.save()
        session_id = request.session.session_key

    return JsonResponse({"key": session_id})
