from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SqliteEmailParityStats:
    inbound_rows: int
    outbound_rows: int
    dead_letter_rows: int


class SqliteEmailParityAdapter:
    """Minimal parity adapter scaffold for email ingestion/delivery state reporting."""

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = str(db_path)

    def load_stats(self) -> SqliteEmailParityStats:
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
