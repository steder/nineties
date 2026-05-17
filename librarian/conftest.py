"""Pytest top-level conftest for the Librarian project.

Test database lives in Postgres via testcontainers; pytest-django reads
DJANGO_SETTINGS_MODULE from pyproject.toml.
"""

from __future__ import annotations

import pytest


@pytest.fixture(scope="session")
def django_db_setup() -> None:
    """Marker placeholder.

    Will be replaced by a testcontainers-based Postgres+pgvector fixture
    when the first integration test lands (plan/0001 day-one task #9 onward).
    For now, unit tests don't hit the DB.
    """
    return None
