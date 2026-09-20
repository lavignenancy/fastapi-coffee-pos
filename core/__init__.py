"""Compatibility package to allow tests to import `core.*`.
This re-exports from `app/core` so absolute imports like `from core.security import ...`
work during pytest collection.
"""
