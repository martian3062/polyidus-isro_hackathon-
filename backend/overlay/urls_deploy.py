from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/overlay-auth/', include('apps.overlay_auth.urls')),
    path('', include('apps.frontend.urls')),
]
