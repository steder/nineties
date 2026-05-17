"""Abstract VoiceAdapter — the pluggable boundary for voice front doors.

Concrete adapters live in subpackages (voice.alexa for v0.1.0; voice.local
for the future Phase 4 local STT/LLM/TTS stack). The active adapter class is
resolved from settings.VOICE_ADAPTER at runtime via `get_adapter()`. Core
code (policy, loans, catalog) must NOT import from any concrete adapter
subpackage — go through this interface instead.

See CLAUDE.md ("Pluggable boundaries — do not violate") and
plans/0001-v0.1.0-audiobook-library.md.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib import import_module
from typing import TYPE_CHECKING

from django.conf import settings

if TYPE_CHECKING:
    from kids.models import Kid
    from loans.models import Loan


@dataclass(frozen=True, slots=True)
class VoiceRequest:
    """A normalized voice request, framework-agnostic.

    Adapters translate their incoming requests (Alexa request JSON, Wyoming
    protocol messages, etc.) into this shape before the core handles them.
    """

    device_id: str  # opaque adapter-scoped identifier; hashed before logging
    intent: str  # canonical intent name: resume | browse | checkout | return | goodnight | help
    slots: dict[str, str]  # arbitrary slot values (e.g., {"book": "The Wild Robot"})


@dataclass(frozen=True, slots=True)
class VoiceResponse:
    """A normalized voice response.

    Adapters translate this into their concrete response format (Alexa
    AudioPlayer directives, etc.).
    """

    say: str  # text to speak (TTS). Empty string for silent responses.
    play_url: str | None = None  # streaming URL for audio playback, if any
    play_offset_seconds: int = 0  # resume offset, if any
    end_session: bool = True  # whether the conversation closes after this response


class VoiceAdapter(ABC):
    """Abstract base class for a voice front door.

    Implementations are responsible for:
      - mapping their device identity to a Kid (lookup, not creation — see
        requirements/safety.md "ID-1: Voice device → kid is explicit")
      - translating intents and slots into VoiceRequest
      - producing playback directives appropriate to their platform
    """

    @abstractmethod
    def resolve_kid(self, request: VoiceRequest) -> Kid | None:
        """Look up the Kid associated with the request's device_id.

        Returns None if no mapping exists. Adapters MUST NOT auto-create
        Kid→device mappings; parents do that explicitly.
        """

    @abstractmethod
    def current_loan(self, kid: Kid) -> Loan | None:
        """Return the kid's most-recently-listened active Loan, if any."""

    @abstractmethod
    def stream_url(self, loan: Loan) -> str:
        """Produce a signed, time-limited streaming URL for the loan's item.

        URL signing details are platform-specific (Alexa needs HTTPS + signed
        token; a local Pi may use a LAN URL with a short-lived token).
        """


def get_adapter() -> VoiceAdapter:
    """Resolve the configured voice adapter class from settings.

    settings.VOICE_ADAPTER is a dotted path to a VoiceAdapter subclass.
    Imports are deferred until call time to keep core code free of any
    concrete-adapter import at module load.
    """
    dotted = settings.VOICE_ADAPTER
    module_path, _, class_name = dotted.rpartition(".")
    if not module_path:
        raise ImportError(
            f"VOICE_ADAPTER must be a dotted path to a VoiceAdapter subclass; got {dotted!r}"
        )
    module = import_module(module_path)
    cls = getattr(module, class_name)
    if not issubclass(cls, VoiceAdapter):
        raise TypeError(f"{dotted} is not a subclass of VoiceAdapter")
    return cls()
