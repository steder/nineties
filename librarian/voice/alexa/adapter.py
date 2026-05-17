"""Alexa concrete voice adapter (v0.1.0).

Implements VoiceAdapter for Amazon Alexa custom skills. Audio playback uses
the Alexa AudioPlayer interface; the streaming URL is produced by the active
MediaBackend (typically AudioBookShelfBackend in v0.1.0).

This module is intentionally a stub at scaffold time. Full implementation
lands as part of plan/0001 day-one task #13 ("Build Alexa skill").
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from voice.adapter import VoiceAdapter, VoiceRequest

if TYPE_CHECKING:
    from kids.models import Kid
    from loans.models import Loan


class AlexaVoiceAdapter(VoiceAdapter):
    """Voice adapter for Amazon Alexa custom skills.

    All Alexa-specific assumptions stay inside this subpackage. Core code
    accesses this adapter only through voice.adapter.get_adapter().
    """

    def resolve_kid(self, request: VoiceRequest) -> Kid | None:
        raise NotImplementedError("AlexaVoiceAdapter.resolve_kid (plan/0001 task #13)")

    def current_loan(self, kid: Kid) -> Loan | None:
        raise NotImplementedError("AlexaVoiceAdapter.current_loan (plan/0001 task #13)")

    def stream_url(self, loan: Loan) -> str:
        raise NotImplementedError("AlexaVoiceAdapter.stream_url (plan/0001 task #13)")
