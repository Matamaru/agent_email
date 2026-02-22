from agent_email.runner import EmailRunner


def test_runner_missing_control_returns_2() -> None:
    rc = EmailRunner().run([])
    assert rc.return_code == 2
    assert rc.output == "missing_control"


def test_runner_inbound_control_returns_ok() -> None:
    rc = EmailRunner().run(["receive"])
    assert rc.return_code == 0
    assert rc.output == "inbound_scaffold:receive"


def test_runner_read_control_returns_ok() -> None:
    rc = EmailRunner().run(["report"])
    assert rc.return_code == 0
    assert rc.output == "read_scaffold:report"


def test_runner_write_controls_default_to_local_guard() -> None:
    rc_send = EmailRunner().run(["send"])
    rc_poll = EmailRunner().run(["poll"])
    assert rc_send.return_code == 41
    assert rc_poll.return_code == 41


def test_runner_write_controls_when_local_disabled_returns_ok() -> None:
    rc_send = EmailRunner(write_local_default=False).run(["send"])
    rc_poll = EmailRunner(write_local_default=False).run(["poll"])
    assert rc_send.return_code == 0
    assert rc_send.output == "write_scaffold:send"
    assert rc_poll.return_code == 0
    assert rc_poll.output == "write_scaffold:poll"
