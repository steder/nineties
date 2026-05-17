from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Items, Tags, and synchronization with the media backend.

    Items represent audiobooks (and later: albums, episodes, films). Tags are
    multi-axis content descriptors that policy uses for eligibility.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
