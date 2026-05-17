"""Media-backend persistence (if any).

v0.1.0 keeps no backend-side state — the AudioBookShelf server is the source
of truth for files/metadata, and our Catalog.Item is the projection. If a
future backend needs per-backend state (e.g., cached ETags, sync cursors),
the model goes here.
"""
