"""Abstract MediaBackend — the pluggable boundary for media servers.

Concrete backends live in sibling modules (media.abs for AudioBookShelf;
media.navidrome and media.jellyfin in future phases). The active backend
class is resolved from settings.MEDIA_BACKEND at runtime via `get_backend()`.
Core code must NOT import from concrete backends — go through this interface.

See CLAUDE.md ("Pluggable boundaries — do not violate") and
plans/0001-v0.1.0-audiobook-library.md.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from importlib import import_module

from django.conf import settings


@dataclass(frozen=True, slots=True)
class BackendItem:
    """Normalized item from a media backend, framework-agnostic.

    Catalog.Item is the persisted projection of this into our DB.
    """

    backend_id: str  # opaque, backend-scoped identifier
    title: str
    author: str
    narrator: str | None
    duration_seconds: int
    cover_url: str | None
    raw: dict[str, object]  # backend-specific extras for debugging/migration


class MediaBackend(ABC):
    """Abstract base class for a media server providing the catalog + audio."""

    @abstractmethod
    def list_items(self) -> Iterator[BackendItem]:
        """Yield all items in the backend's library.

        Implementations should paginate transparently and yield as they go;
        callers may consume the iterator lazily.
        """

    @abstractmethod
    def stream_url(self, backend_id: str, *, offset_seconds: int = 0) -> str:
        """Produce a streaming URL for the given item.

        URLs should be time-limited / signed; never return URLs that grant
        permanent access to the backend.
        """

    @abstractmethod
    def healthcheck(self) -> bool:
        """Return True iff the backend is reachable and responsive."""


def get_backend() -> MediaBackend:
    """Resolve the configured media backend class from settings.

    settings.MEDIA_BACKEND is a dotted path to a MediaBackend subclass.
    Imports are deferred until call time to keep core code free of any
    concrete-backend import at module load.
    """
    dotted = settings.MEDIA_BACKEND
    module_path, _, class_name = dotted.rpartition(".")
    if not module_path:
        raise ImportError(
            f"MEDIA_BACKEND must be a dotted path to a MediaBackend subclass; got {dotted!r}"
        )
    module = import_module(module_path)
    cls = getattr(module, class_name)
    if not issubclass(cls, MediaBackend):
        raise TypeError(f"{dotted} is not a subclass of MediaBackend")
    return cls()
