"""Scaffold-level smoke tests.

These tests prove the project loads cleanly. They do NOT exercise app logic
(which doesn't exist yet); they're here so `just smoke` and `just test` have
something to run from day one and CI is non-trivially green.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.smoke


def test_django_settings_loads() -> None:
    """Django settings module imports without error."""
    from django.conf import settings

    assert settings.SECRET_KEY  # must be set via env, not the insecure default
    assert "policy" in settings.INSTALLED_APPS
    assert "catalog" in settings.INSTALLED_APPS
    assert "kids" in settings.INSTALLED_APPS
    assert "loans" in settings.INSTALLED_APPS
    assert "voice" in settings.INSTALLED_APPS
    assert "media" in settings.INSTALLED_APPS


def test_voice_adapter_dotted_path_resolves() -> None:
    """The default VOICE_ADAPTER setting resolves to a VoiceAdapter subclass."""
    from voice.adapter import VoiceAdapter, get_adapter

    adapter = get_adapter()
    assert isinstance(adapter, VoiceAdapter)


def test_media_backend_dotted_path_resolves() -> None:
    """The default MEDIA_BACKEND setting resolves to a MediaBackend subclass."""
    from media.backend import MediaBackend, get_backend

    backend = get_backend()
    assert isinstance(backend, MediaBackend)


def test_core_does_not_import_concrete_adapters() -> None:
    """Core packages must not import from concrete adapter/backend subpackages.

    This is a structural test for the pluggability invariant. If any module in
    catalog/, kids/, loans/, or policy/ ever does `from voice.alexa import ...`
    or `from media.abs import ...`, this test will fail.
    """
    import ast
    from pathlib import Path

    forbidden = {"voice.alexa", "media.abs"}
    core_packages = {"catalog", "kids", "loans", "policy"}
    repo = Path(__file__).resolve().parent.parent.parent

    offenders: list[tuple[str, str]] = []
    for pkg in core_packages:
        for py in (repo / pkg).rglob("*.py"):
            tree = ast.parse(py.read_text(), filename=str(py))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    if any(node.module == f or node.module.startswith(f + ".") for f in forbidden):
                        offenders.append((str(py.relative_to(repo)), node.module))
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if any(
                            alias.name == f or alias.name.startswith(f + ".")
                            for f in forbidden
                        ):
                            offenders.append((str(py.relative_to(repo)), alias.name))

    assert not offenders, (
        "Core packages must not import concrete adapter/backend modules. "
        f"Violations: {offenders}"
    )
