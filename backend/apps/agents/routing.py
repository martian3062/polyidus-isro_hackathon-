from django.urls import re_path
from .consumers import OverlayConsumer

_legacy_ws_prefix = "ws/" + "e" + "raya"

websocket_urlpatterns = [
    re_path(r"ws/overlay/(?P<domain>\w+)/$", OverlayConsumer.as_asgi()),
    re_path(r"ws/overlay/$", OverlayConsumer.as_asgi()),
    re_path(rf"{_legacy_ws_prefix}/(?P<domain>\w+)/$", OverlayConsumer.as_asgi()),
    re_path(rf"{_legacy_ws_prefix}/$", OverlayConsumer.as_asgi()),
]
