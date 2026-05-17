from django.apps import AppConfig


class LoansConfig(AppConfig):
    """Loan lifecycle: checkout, return, expiry, listening progress.

    Enforces the invariants in requirements/safety.md (loan caps,
    no double-borrow, progress preservation across returns, cooldown).
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "loans"
