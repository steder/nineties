"""Voice models — per-adapter persistent state lives here, not in core.

When the Alexa adapter needs to persist e.g. a session-id-to-loan mapping for
multi-turn conversations, the model goes here (or in voice/alexa/models.py if
it's adapter-specific). The point is to keep adapter-specific fields out of
core models (Kid, Item, Loan).
"""
