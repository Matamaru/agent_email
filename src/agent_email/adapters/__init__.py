"""Adapters for agent_email integration points."""

from .sqlite_parity import SqliteEmailParityAdapter, SqliteEmailParityStats

__all__ = ["SqliteEmailParityAdapter", "SqliteEmailParityStats"]
