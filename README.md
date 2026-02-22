# agent_email

A focused Python scaffold for email control routing and basic SQLite parity reporting.

This repository is intentionally small: it gives you stable contracts and predictable placeholder behavior while upstream email workflows are being extracted and hardened.

## What You Get

- Control contracts for inbound, outbound, loop, and read actions
- Predicate helpers to validate controls
- `EmailRunner` scaffold for routing controls with safe write defaults
- SQLite parity adapter for quick queue/state counters

## Installation

```bash
pip install -e .
```

Install with development dependencies (tests):

```bash
pip install -e .[dev]
```

## Quick Start

### 1. Validate controls

```python
from agent_email.contracts import is_inbound_control, is_read_control

assert is_inbound_control("receive") is True
assert is_read_control("report") is True
assert is_inbound_control("send") is False
```

### 2. Run scaffold control dispatch

```python
from agent_email.runner import EmailRunner

runner = EmailRunner()

print(runner.run(["receive"]))  # EmailCommandResult(return_code=0, output='inbound_scaffold:receive')
print(runner.run(["report"]))   # EmailCommandResult(return_code=0, output='read_scaffold:report')
print(runner.run(["send"]))     # EmailCommandResult(return_code=41, output='write_local_default:send')
```

Disable write-local guard when you explicitly want write scaffolds:

```python
from agent_email.runner import EmailRunner

runner = EmailRunner(write_local_default=False)
print(runner.run(["poll"]))  # EmailCommandResult(return_code=0, output='write_scaffold:poll')
```

### 3. Read parity stats from SQLite

```python
import sqlite3
from pathlib import Path

from agent_email.adapters.sqlite_parity import SqliteEmailParityAdapter

db_path = Path("parity.db")
with sqlite3.connect(str(db_path)) as conn:
    conn.execute("CREATE TABLE email_messages (message_id TEXT PRIMARY KEY, direction TEXT NOT NULL)")
    conn.execute("CREATE TABLE email_dead_letters (dead_letter_id TEXT PRIMARY KEY, kind TEXT NOT NULL)")
    conn.execute("INSERT INTO email_messages(message_id, direction) VALUES ('m1', 'inbound')")
    conn.execute("INSERT INTO email_messages(message_id, direction) VALUES ('m2', 'outbound')")
    conn.execute("INSERT INTO email_dead_letters(dead_letter_id, kind) VALUES ('d1', 'email_send')")
    conn.commit()

stats = SqliteEmailParityAdapter(db_path).load_stats()
print(stats.inbound_rows, stats.outbound_rows, stats.dead_letter_rows)
```

## Runner Return Codes

- `0`: recognized control, scaffold handled successfully
- `2`: missing or unsupported control
- `41`: write-like control blocked by safe local default

## API Docs

Detailed API documentation is in `api.md`.

## Development

Run tests:

```bash
pytest -q
```

The project uses:
- Python `>=3.11`
- `setuptools` build backend
- `pytest` as optional dev dependency

## Current Scope and Caveats

- This is a scaffold package: outputs are structured placeholders, not final production side effects.
- The SQLite adapter expects specific table names and minimal columns:
  - `email_messages(direction)`
  - `email_dead_letters(...)`

## License

MIT
