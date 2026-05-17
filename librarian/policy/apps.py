from django.apps import AppConfig


class PolicyConfig(AppConfig):
    """Policy is pure logic — no models of its own.

    Eligibility/tagging functions live here and are imported by `loans`
    and the voice adapter. See requirements/safety.md for the invariants
    this app must guarantee.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "policy"
