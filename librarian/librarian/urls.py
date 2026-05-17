"""URL configuration for the Librarian service."""

from django.contrib import admin
from django.http import HttpRequest, JsonResponse
from django.urls import path


def health(_request: HttpRequest) -> JsonResponse:
    """Liveness probe used by Compose healthcheck and CI smoke."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    # Voice-adapter and parent-UI routes will be added by individual apps' urls.py
    # as those apps land. Kept minimal here to avoid premature routing.
]
