"""Email control contract constants and control-group predicates."""

from __future__ import annotations

EMAIL_INBOUND_CONTROLS: tuple[str, ...] = (
    "receive",
    "triage",
)

EMAIL_OUTBOUND_CONTROLS: tuple[str, ...] = (
    "send",
    "retry-outbound",
)

EMAIL_LOOP_CONTROLS: tuple[str, ...] = (
    "poll",
)

EMAIL_READ_CONTROLS: tuple[str, ...] = (
    "report",
)


def is_inbound_control(control: str) -> bool:
    """Return whether `control` is an inbound email control."""
    return control in EMAIL_INBOUND_CONTROLS


def is_outbound_control(control: str) -> bool:
    """Return whether `control` is an outbound email control."""
    return control in EMAIL_OUTBOUND_CONTROLS


def is_loop_control(control: str) -> bool:
    """Return whether `control` is a loop/polling control."""
    return control in EMAIL_LOOP_CONTROLS


def is_read_control(control: str) -> bool:
    """Return whether `control` is a read/reporting control."""
    return control in EMAIL_READ_CONTROLS
