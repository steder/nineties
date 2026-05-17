"""Catalog models — Item and Tag.

Stub at scaffold time. Fleshed out as part of plan/0001 day-one task #9
("Create catalog app: Item, Tag, ABS sync management command").

Planned shape (from plans/0001-v0.1.0-audiobook-library.md):
    Tag   (id, key, value, axis)
    Item  (id, abs_id, title, author, narrator, duration, cover,
           tags M2M, embedding pgvector(768))
"""
