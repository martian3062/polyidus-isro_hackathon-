from django.urls import path
from .views import AirgapStatusView, AttackSimView, SpoofSimView

urlpatterns = [
    path("attack-sim/", AttackSimView.as_view(), name="overlay-shield-attack-sim"),
    path("spoof-sim/",  SpoofSimView.as_view(),  name="overlay-shield-spoof-sim"),
    path("airgap-status/", AirgapStatusView.as_view(), name="airgap-status"),
]
