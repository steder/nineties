"""Step definitions for tests/features/kid_checks_out_book.feature.

All steps are stubs (pytest.skip) until the corresponding code lands. The
feature file itself is the load-bearing spec — see CLAUDE.md "Test layering"
and plans/0001-v0.1.0-audiobook-library.md "Testing strategy".
"""

from __future__ import annotations

import pytest
from pytest_bdd import scenarios

# Bind every scenario in the feature file to this test module. Each scenario
# becomes a test; missing step definitions cause an explicit collection-time
# error, which is what we want at scaffold time.
scenarios("../features/kid_checks_out_book.feature")


# When the implementer-agent picks up plan/0001 task #9 onward, they'll add
# @given / @when / @then handlers below and remove the xfail marker.
pytestmark = pytest.mark.bdd
