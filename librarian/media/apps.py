from django.apps import AppConfig


class MediaConfig(AppConfig):
    """Media backend abstraction and concrete backend implementations.

    Core code never imports from a concrete backend module. The active
    backend class is resolved from settings.MEDIA_BACKEND at runtime via
    media.backend.get_backend().

    Concrete backends:
      - media.abs.AudioBookShelfBackend  (v0.1.0 default)
      - media.navidrome (Phase 2)
      - media.jellyfin  (Phase 5)
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "media"
