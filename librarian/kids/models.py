"""Kids models — Kid and Policy.

Minimal placeholder; full schema lands in plan/0001 task #10
("Create kids app: Kid, Policy, Django admin editing").

Planned shape:
    Kid     (id, name, birthdate, alexa_device_ids[], active, ...)
    Policy  (id, kid_id FK, axis, max_value, mode allow|deny|require_review)
"""

from django.db import models


class Kid(models.Model):
    """A child user of the system.

    Placeholder: name only. Full fields land with plan/0001 task #10.
    """

    name = models.CharField(max_length=100)

    class Meta:
        app_label = "kids"

    def __str__(self) -> str:
        return self.name
