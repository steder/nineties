from django.apps import AppConfig


class KidsConfig(AppConfig):
    """Kid identity and per-kid Policy.

    A Kid is NOT a Django auth user; it is identified by the voice adapter
    device IDs mapped to it (e.g., Alexa device IDs). Parents (auth.User) own
    Kid records and manage their policy.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "kids"
