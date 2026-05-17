"""Policy has no models of its own — it is pure logic.

Eligibility functions live in policy/eligibility.py (to be added with the
loans app). The Policy *record* (per-kid configuration) lives in the kids app
since it is keyed on Kid.
"""
