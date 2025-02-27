"""Role testing files using testinfra."""

import pytest
import testinfra.host

GOSS = "goss"


@pytest.fixture
def executable(host: testinfra.host) -> str:
    """Check and return Goss bin."""
    try:
        return host.find_command(GOSS)
    except ValueError as ex:
        pytest.fail(str(ex), pytrace=False)
    return None


def test_goss(host: testinfra.host, executable: str):  # pylint: disable=redefined-outer-name
    """Check Goss is zerover and major verions has not changed."""
    goss_minor_ver = 4
    cmd = host.run(f"{executable} --version")
    cmd_ver = cmd.stdout.split()[-1]

    assert cmd.succeeded
    assert cmd_ver.split(".")[0] == "v0"
    assert int(cmd_ver.split(".")[1]) > goss_minor_ver
    assert not cmd.stderr


def test_run_example(
    host: testinfra.host,
    executable: str,  # pylint: disable=redefined-outer-name
) :
    """Run Goss example test."""
    cmd = host.run(f"{executable} --gossfile /usr/share/goss/goss.yaml validate --format tap")

    assert cmd.succeeded
    assert not cmd.stderr
