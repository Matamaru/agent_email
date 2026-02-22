import sqlite3

from agent_email.adapters.sqlite_parity import SqliteEmailParityAdapter


def test_sqlite_email_parity_adapter_counts_rows(tmp_path) -> None:
    db_path = tmp_path / "parity.db"
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE email_messages (
                message_id TEXT PRIMARY KEY,
                direction TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE email_dead_letters (
                dead_letter_id TEXT PRIMARY KEY,
                kind TEXT NOT NULL
            )
            """
        )
        conn.execute("INSERT INTO email_messages(message_id, direction) VALUES ('m1', 'inbound')")
        conn.execute("INSERT INTO email_messages(message_id, direction) VALUES ('m2', 'outbound')")
        conn.execute("INSERT INTO email_messages(message_id, direction) VALUES ('m3', 'outbound')")
        conn.execute("INSERT INTO email_dead_letters(dead_letter_id, kind) VALUES ('d1', 'email_send')")
        conn.commit()

    stats = SqliteEmailParityAdapter(db_path).load_stats()
    assert stats.inbound_rows == 1
    assert stats.outbound_rows == 2
    assert stats.dead_letter_rows == 1
