from django.apps import AppConfig


class VoiceConfig(AppConfig):
    """Voice adapter abstraction and concrete adapter implementations.

    Core code never imports from a concrete adapter subpackage. The active
    adapter class is resolved from settings.VOICE_ADAPTER at runtime via
    voice.adapter.get_adapter().

    Concrete adapters:
      - voice.alexa.AlexaVoiceAdapter  (v0.1.0 default; Alexa custom skill)
      - voice.local.LocalVoiceAdapter   (future: Phase 4, Wyoming-protocol-based)
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "voice"
