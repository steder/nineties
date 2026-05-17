"""Alexa voice adapter — the v0.1.0 default.

This subpackage MUST NOT be imported from core code (policy, loans, catalog,
kids). The active adapter is resolved by settings.VOICE_ADAPTER through
voice.adapter.get_adapter().
"""

from voice.alexa.adapter import AlexaVoiceAdapter

__all__ = ["AlexaVoiceAdapter"]
