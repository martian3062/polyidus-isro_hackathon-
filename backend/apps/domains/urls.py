from django.urls import path
from . import views

urlpatterns = [
    path("", views.domain_list, name="domain-list"),
    path("<str:domain>/status/", views.domain_status, name="domain-status"),
    path("<str:domain>/signals/", views.domain_signals, name="domain-signals"),
    path("<str:domain>/actions/", views.domain_actions, name="domain-actions"),
    path("<str:domain>/topology/", views.domain_topology, name="domain-topology"),
    path("<str:domain>/flow-divergence/", views.domain_flow_divergence, name="domain-flow-divergence"),
    path("<str:domain>/forecasts/", views.domain_forecasts, name="domain-forecasts"),
    path("<str:domain>/telemetry/", views.domain_telemetry_snapshot, name="domain-telemetry"),
    path("<str:domain>/inject-fault/", views.domain_inject_fault, name="domain-inject-fault"),
]
