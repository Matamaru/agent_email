from __future__ import annotations

from dataclasses import dataclass

from .contracts import (
    EMAIL_INBOUND_CONTROLS,
    EMAIL_LOOP_CONTROLS,
    EMAIL_READ_CONTROLS,
    EMAIL_OUTBOUND_CONTROLS,
    is_inbound_control,
    is_loop_control,
    is_read_control,
    is_outbound_control,
)


@dataclass(frozen=True)
class EmailCommandResult:
    return_code: int
    output: str


class EmailRunner:
    """Stage 19.2 scaffold runner for extracted email control dispatch."""

    def __init__(self, *, write_local_default: bool = True) -> None:
        self._write_local_default = bool(write_local_default)

    @property
    def supported_inbound_controls(self) -> tuple[str, ...]:
        return EMAIL_INBOUND_CONTROLS

    @property
    def supported_outbound_controls(self) -> tuple[str, ...]:
        return EMAIL_OUTBOUND_CONTROLS

    @property
    def supported_loop_controls(self) -> tuple[str, ...]:
        return EMAIL_LOOP_CONTROLS

    @property
    def supported_read_controls(self) -> tuple[str, ...]:
        return EMAIL_READ_CONTROLS

    def run(self, argv: list[str]) -> EmailCommandResult:
        if not argv:
            return EmailCommandResult(return_code=2, output="missing_control")
        control = str(argv[0]).strip()
        if is_read_control(control):
            return EmailCommandResult(return_code=0, output=f"read_scaffold:{control}")
        if is_inbound_control(control):
            return EmailCommandResult(return_code=0, output=f"inbound_scaffold:{control}")
        if is_outbound_control(control) or is_loop_control(control):
            if self._write_local_default:
                return EmailCommandResult(return_code=41, output=f"write_local_default:{control}")
            return EmailCommandResult(return_code=0, output=f"write_scaffold:{control}")
        return EmailCommandResult(return_code=2, output=f"unsupported_control:{control}")
