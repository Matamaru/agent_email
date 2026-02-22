"""SQLite adapter for minimal email parity and queue state counts."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SqliteEmailParityStats:
    """Materialized parity counters read from the SQLite email store.

    Attributes:
        inbound_rows: Number of `email_messages` rows with `direction='inbound'`.
        outbound_rows: Number of `email_messages` rows with `direction='outbound'`.
        dead_letter_rows: Number of rows in `email_dead_letters`.
    """

    inbound_rows: int
    outbound_rows: int
    dead_letter_rows: int


class SqliteEmailParityAdapter:
    """Read-only adapter that reports queue/state counts from SQLite tables."""

    def __init__(self, db_path: str | Path) -> None:
        """Create an adapter bound to a SQLite database path."""
        self._db_path = str(db_path)

    def load_stats(self) -> SqliteEmailParityStats:
        """Query the database and return current parity row counts."""
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            inbound_rows = int(conn.execute("SELECT COUNT(*) FROM email_messages WHERE direction = 'inbound'").fetchone()[0])
            outbound_rows = int(conn.execute("SELECT COUNT(*) FROM email_messages WHERE direction = 'outbound'").fetchone()[0])
            dead_letter_rows = int(conn.execute("SELECT COUNT(*) FROM email_dead_letters").fetchone()[0])
        return SqliteEmailParityStats(
            inbound_rows=inbound_rows,
            outbound_rows=outbound_rows,
            dead_letter_rows=dead_letter_rows,
        )
