"""AudioBookShelf concrete media backend (v0.1.0).

Implements MediaBackend against the AudioBookShelf HTTP API. All ABS-specific
assumptions stay inside this module. Core code accesses this backend only
through media.backend.get_backend().

This module is a stub at scaffold time. Full implementation lands as part of
plan/0001 day-one task #9 ("Create catalog app: ABS sync management command").

API reference: https://api.audiobookshelf.org/
"""

from __future__ import annotations

from collections.abc import Iterator

from media.backend import BackendItem, MediaBackend


class AudioBookShelfBackend(MediaBackend):
    """Media backend backed by an AudioBookShelf server."""

    def list_items(self) -> Iterator[BackendItem]:
        raise NotImplementedError("AudioBookShelfBackend.list_items (plan/0001 task #9)")

    def stream_url(self, backend_id: str, *, offset_seconds: int = 0) -> str:
        raise NotImplementedError("AudioBookShelfBackend.stream_url (plan/0001 task #9)")

    def healthcheck(self) -> bool:
        raise NotImplementedError("AudioBookShelfBackend.healthcheck (plan/0001 task #9)")
