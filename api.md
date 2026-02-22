# API Reference: `agent_email`

`agent_email` is a small Python package that exposes:
- control contracts (allowed control names + predicates)
- an execution scaffold runner (`EmailRunner`)
- a SQLite parity adapter for basic state counts

## Install

```bash
pip install -e .
```

For tests/dev tooling:

```bash
pip install -e .[dev]
```

## Module: `agent_email.contracts`

### Constants

- `EMAIL_INBOUND_CONTROLS: tuple[str, ...]`
  - Current values: `("receive", "triage")`
- `EMAIL_OUTBOUND_CONTROLS: tuple[str, ...]`
  - Current values: `("send", "retry-outbound")`
- `EMAIL_LOOP_CONTROLS: tuple[str, ...]`
  - Current values: `("poll",)`
- `EMAIL_READ_CONTROLS: tuple[str, ...]`
  - Current values: `("report",)`

### Predicates

- `is_inbound_control(control: str) -> bool`
- `is_outbound_control(control: str) -> bool`
- `is_loop_control(control: str) -> bool`
- `is_read_control(control: str) -> bool`

These helpers validate whether a control belongs to a specific contract group.

Example:

```python
from agent_email.contracts import is_inbound_control, is_outbound_control

assert is_inbound_control("receive") is True
assert is_outbound_control("receive") is False
```

## Module: `agent_email.runner`

### Class: `EmailCommandResult`

Dataclass returned by `EmailRunner.run(argv)`.

Fields:
- `return_code: int`
- `output: str`

### Class: `EmailRunner`

```python
EmailRunner(*, write_local_default: bool = True)
```

Purpose:
- routes a single control token from `argv[0]`
- enforces safe default behavior for write-like actions (`send`, `retry-outbound`, `poll`)

Properties:
- `supported_inbound_controls -> tuple[str, ...]`
- `supported_outbound_controls -> tuple[str, ...]`
- `supported_loop_controls -> tuple[str, ...]`
- `supported_read_controls -> tuple[str, ...]`

Method:
- `run(argv: list[str]) -> EmailCommandResult`

Behavior matrix:

| Input | Condition | return_code | output |
|---|---|---:|---|
| `[]` | missing control | `2` | `missing_control` |
| `report` | read control | `0` | `read_scaffold:report` |
| `receive` / `triage` | inbound control | `0` | `inbound_scaffold:<control>` |
| `send` / `retry-outbound` / `poll` with default runner | write guard active | `41` | `write_local_default:<control>` |
| `send` / `retry-outbound` / `poll` with `write_local_default=False` | write guard disabled | `0` | `write_scaffold:<control>` |
| any other control | unsupported | `2` | `unsupported_control:<control>` |

Example: safe default mode

```python
from agent_email.runner import EmailRunner

runner = EmailRunner()  # write_local_default=True
result = runner.run(["send"])

assert result.return_code == 41
assert result.output == "write_local_default:send"
```

Example: allow write scaffolds

```python
from agent_email.runner import EmailRunner

runner = EmailRunner(write_local_default=False)
result = runner.run(["poll"])

assert result.return_code == 0
assert result.output == "write_scaffold:poll"
```

## Module: `agent_email.adapters.sqlite_parity`

### Class: `SqliteEmailParityStats`

Dataclass with aggregated counts:
- `inbound_rows: int`
- `outbound_rows: int`
- `dead_letter_rows: int`

### Class: `SqliteEmailParityAdapter`

```python
SqliteEmailParityAdapter(db_path: str | pathlib.Path)
```

Methods:
- `load_stats() -> SqliteEmailParityStats`

Expected schema:
- table `email_messages` with column `direction`
- table `email_dead_letters`

Example:

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
assert stats.inbound_rows == 1
assert stats.outbound_rows == 1
assert stats.dead_letter_rows == 1
```

## Package Exports

- `agent_email.__version__`
- `agent_email.adapters.SqliteEmailParityAdapter`
- `agent_email.adapters.SqliteEmailParityStats`

