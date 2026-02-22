from agent_email.contracts import (
    EMAIL_INBOUND_CONTROLS,
    EMAIL_LOOP_CONTROLS,
    EMAIL_READ_CONTROLS,
    EMAIL_OUTBOUND_CONTROLS,
    is_inbound_control,
    is_loop_control,
    is_read_control,
    is_outbound_control,
)


def test_email_contract_controls_exposed() -> None:
    assert "receive" in EMAIL_INBOUND_CONTROLS
    assert "send" in EMAIL_OUTBOUND_CONTROLS
    assert "poll" in EMAIL_LOOP_CONTROLS
    assert "report" in EMAIL_READ_CONTROLS


def test_email_contract_predicates() -> None:
    assert is_inbound_control("triage") is True
    assert is_inbound_control("send") is False
    assert is_outbound_control("send") is True
    assert is_outbound_control("receive") is False
    assert is_loop_control("poll") is True
    assert is_read_control("report") is True
