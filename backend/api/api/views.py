from django.core.cache import cache


def get_example_network(request):
    return cache.get("network")


def get_distribution_for_node(request, node: str):
    return cache.get(f"prior-distribution-{node}")
