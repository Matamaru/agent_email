"""Email control runner scaffold and result contract."""

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
    """Result payload for one control invocation.

    Attributes:
        return_code: Exit-code style integer for the invoked control.
        output: Machine-readable scaffold message for downstream handling.
    """

    return_code: int
    output: str


class EmailRunner:
    """Dispatch scaffold email controls to their current placeholder behavior.

    The runner groups controls by intent:
    - read controls return a read scaffold response
    - inbound controls return an inbound scaffold response
    - outbound and loop controls are guarded by `write_local_default`
    """

    def __init__(self, *, write_local_default: bool = True) -> None:
        """Initialize runner behavior for write controls."""
        self._write_local_default = bool(write_local_default)

    @property
    def supported_inbound_controls(self) -> tuple[str, ...]:
        """Supported control names for inbound operations."""
        return EMAIL_INBOUND_CONTROLS

    @property
    def supported_outbound_controls(self) -> tuple[str, ...]:
        """Supported control names for outbound operations."""
        return EMAIL_OUTBOUND_CONTROLS

    @property
    def supported_loop_controls(self) -> tuple[str, ...]:
        """Supported control names for loop/poll operations."""
        return EMAIL_LOOP_CONTROLS

    @property
    def supported_read_controls(self) -> tuple[str, ...]:
        """Supported control names for read/report operations."""
        return EMAIL_READ_CONTROLS

    def run(self, argv: list[str]) -> EmailCommandResult:
        """Dispatch the first CLI argument to the matching scaffold control."""
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
