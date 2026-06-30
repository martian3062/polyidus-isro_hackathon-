from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .registry import get_registered_domains, get_domain


@api_view(["GET"])
@permission_classes([AllowAny])
def domain_list(request):
    domains = get_registered_domains()
    return Response({"domains": [
        {"name": d, "status": "active"} for d in domains
    ]})


@api_view(["GET"])
@permission_classes([AllowAny])
def domain_status(request, domain: str):
    env = get_domain(domain)
    if env is None:
        return Response({"error": f"Domain '{domain}' not registered"}, status=404)
    return Response(env.health_check())


@api_view(["GET"])
@permission_classes([AllowAny])
def domain_signals(request, domain: str):
    env = get_domain(domain)
    if env is None:
        return Response({"error": f"Domain '{domain}' not found"}, status=404)
    signals = []
    for i, sig in enumerate(env.signal_stream()):
        signals.append({
            "timestamp": sig.timestamp,
            "source": sig.source,
            "features": sig.features,
        })
        if i >= 9:
            break
    return Response({"domain": domain, "signals": signals})


@api_view(["GET"])
@permission_classes([AllowAny])
def domain_actions(request, domain: str):
    env = get_domain(domain)
    if env is None:
        return Response({"error": f"Domain '{domain}' not found"}, status=404)
    return Response({"domain": domain, "actions": env.available_actions()})


@api_view(["GET"])
@permission_classes([AllowAny])
def domain_topology(request, domain: str):
    env = get_domain(domain)
    if env is None:
        return Response({"error": f"Domain '{domain}' not found"}, status=404)
    if not hasattr(env, "topology"):
        return Response({"error": f"Domain '{domain}' has no topology view"}, status=404)
    return Response({"domain": domain, "topology": env.topology()})


@api_view(["GET"])
@permission_classes([AllowAny])
def domain_flow_divergence(request, domain: str):
    env = get_domain(domain)
    if env is None:
        return Response({"error": f"Domain '{domain}' not found"}, status=404)
    if not hasattr(env, "flow_divergence"):
        return Response({"error": f"Domain '{domain}' has no flow divergence view"}, status=404)
    return Response({"domain": domain, "flow_divergence": env.flow_divergence()})


@api_view(["GET"])
@permission_classes([AllowAny])
def domain_forecasts(request, domain: str):
    env = get_domain(domain)
    if env is None:
        return Response({"error": f"Domain '{domain}' not found"}, status=404)
    if not hasattr(env, "forecasts"):
        return Response({"error": f"Domain '{domain}' has no forecast view"}, status=404)
    return Response({"domain": domain, "forecasts": env.forecasts()})


@api_view(["GET"])
@permission_classes([AllowAny])
def domain_telemetry_snapshot(request, domain: str):
    env = get_domain(domain)
    if env is None:
        return Response({"error": f"Domain '{domain}' not found"}, status=404)
    if not hasattr(env, "telemetry_snapshot"):
        return Response({"error": f"Domain '{domain}' has no telemetry snapshot"}, status=404)
    window_seconds = int(request.GET.get("window_seconds", "300"))
    return Response({"domain": domain, **env.telemetry_snapshot(window_seconds)})


@api_view(["POST"])
@permission_classes([AllowAny])
def domain_inject_fault(request, domain: str):
    env = get_domain(domain)
    if env is None:
        return Response({"error": f"Domain '{domain}' not found"}, status=404)
    if not hasattr(env, "inject_fault"):
        return Response({"error": f"Domain '{domain}' has no fault injection"}, status=404)
    scenario_id = request.data.get("scenario_id", "progressive_congestion")
    return Response({"domain": domain, **env.inject_fault(scenario_id)})
